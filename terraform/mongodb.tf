resource "mongodbatlas_advanced_cluster" "this" {
  project_id   = var.mongodb_project_id
  name         = var.name
  cluster_type = "REPLICASET"

  replication_specs {
    region_configs {
      priority              = 7
      provider_name         = "TENANT"
      region_name           = "EUROPE_WEST"
      backing_provider_name = "AZURE"

      electable_specs {
        instance_size = "M0"
      }
    }
  }
}

locals {
  mongodb_url = split("//", split(",", mongodbatlas_advanced_cluster.this.connection_strings[0].standard)[0])[1]
}

resource "mongodbatlas_project_ip_access_list" "anyone" {
  project_id = var.mongodb_project_id
  cidr_block = "0.0.0.0/0"
  comment    = "Do not filter by ip"
}

resource "mongodbatlas_database_user" "admin" {
  username           = var.mongodb_user_admin.username
  password           = var.mongodb_user_admin.password
  project_id         = var.mongodb_project_id
  auth_database_name = "admin"

  roles {
    role_name     = "atlasAdmin"
    database_name = "admin"
  }

  scopes {
    name = mongodbatlas_advanced_cluster.this.name
    type = "CLUSTER"
  }

  provisioner "local-exec" {
    when = create

    command     = "bash python_venv.sh create.py"
    working_dir = "./mongodb_data"
    environment = {
      MONGODB_URI = nonsensitive("mongodb://${var.mongodb_user_admin.username}:${var.mongodb_user_admin.password}@${local.mongodb_url}?tls=true")
      FILE_PATH   = "./it.json"
    }
  }

  depends_on = [
    mongodbatlas_project_ip_access_list.anyone,
    mongodbatlas_advanced_cluster.this
  ]
}

resource "mongodbatlas_database_user" "core" {
  username           = var.mongodb_user_core.username
  password           = var.mongodb_user_core.password
  project_id         = var.mongodb_project_id
  auth_database_name = "admin"

  roles {
    role_name     = "read"
    database_name = "pictograms"
  }

  scopes {
    name = mongodbatlas_advanced_cluster.this.name
    type = "CLUSTER"
  }

  depends_on = [
    mongodbatlas_project_ip_access_list.anyone,
    mongodbatlas_advanced_cluster.this
  ]
}

