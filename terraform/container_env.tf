resource "azurerm_virtual_network" "container_env" {
  name                = "${var.name}-container_env"
  address_space       = ["10.0.0.0/16"]
  location            = var.location
  resource_group_name = azurerm_resource_group.this.name
}

resource "azurerm_subnet" "container" {
  name                 = "container"
  resource_group_name  = azurerm_resource_group.this.name
  virtual_network_name = azurerm_virtual_network.container_env.name
  address_prefixes     = ["10.0.2.0/24"]
  service_endpoints    = ["Microsoft.KeyVault"]

  delegation {
    name = "Microsoft.App.environments"
    service_delegation {
      name = "Microsoft.App/environments"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action",
      ]
    }
  }
}

locals {
  workload_profile_name = "Consumption"
}

resource "azurerm_container_app_environment" "this" {
  name                     = var.name
  location                 = var.location
  resource_group_name      = azurerm_resource_group.this.name
  infrastructure_subnet_id = azurerm_subnet.container.id

  workload_profile {
    name                  = local.workload_profile_name
    workload_profile_type = local.workload_profile_name
  }

  lifecycle {
    ignore_changes = [infrastructure_resource_group_name] # let Azure create a RG for it
  }
}

locals {
  gh_username = split("/", var.gh_minio_repo)[3]
}


resource "azurerm_container_app" "core" {
  name                         = local.repos[var.gh_core_repo]
  container_app_environment_id = azurerm_container_app_environment.this.id
  resource_group_name          = azurerm_resource_group.this.name
  revision_mode                = "Single"

  ingress {
    external_enabled           = false
    allow_insecure_connections = true
    target_port                = 80
    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  registry {
    identity = azurerm_user_assigned_identity.this[var.gh_core_repo].id
    server   = azurerm_container_registry.this.login_server
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.this[var.gh_core_repo].id]
  }

  template {
    container {
      name   = local.repos[var.gh_core_repo]
      image  = "${azurerm_container_registry.this.login_server}/${azurerm_container_registry_task.build_image[var.gh_core_repo].docker_step[0].image_names[0]}"
      cpu    = 1
      memory = "2Gi"

      env {
        name  = "MONGODB_URI"
        value = "mongodb://${var.mongodb_user_core.username}:${var.mongodb_user_core.password}@${local.mongodb_url}?tls=true"
      }
      env {
        name  = "MONGODB_DATABASE"
        value = "pictograms"
      }
      env {
        name  = "MONGODB_COLLECTION"
        value = "pictograms"
      }
    }
    min_replicas = var.scale.min
    max_replicas = var.scale.max
  }

  workload_profile_name = local.workload_profile_name

  depends_on = [
    azurerm_container_registry_task_schedule_run_now.build_image,
    azurerm_role_assignment.acr_pull,
    mongodbatlas_database_user.core,
    mongodbatlas_project_ip_access_list.anyone,
    mongodbatlas_advanced_cluster.this
  ]
}

resource "azurerm_container_app" "minio" {
  name                         = local.repos[var.gh_minio_repo]
  container_app_environment_id = azurerm_container_app_environment.this.id
  resource_group_name          = azurerm_resource_group.this.name
  revision_mode                = "Single"

  ingress {
    external_enabled           = true
    allow_insecure_connections = true
    target_port                = 9000
    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.this[var.gh_minio_repo].id]
  }


  registry {
    server               = "ghcr.io"
    username             = local.gh_username
    password_secret_name = local.secK_gh_access_token
  }

  secret {
    identity            = azurerm_user_assigned_identity.this[var.gh_minio_repo].id
    name                = local.secK_gh_access_token
    key_vault_secret_id = azurerm_key_vault_secret.this[local.secK_gh_access_token].id
  }

  template {
    container {
      name   = local.repos[var.gh_minio_repo]
      image  = "ghcr.io/${local.gh_username}/${split("/", var.gh_minio_repo)[4]}:latest"
      cpu    = 1
      memory = "2Gi"
    }
    min_replicas = var.scale.min
    max_replicas = var.scale.max
  }

  workload_profile_name = local.workload_profile_name

  depends_on = [
    azurerm_role_assignment.minio_secrets
  ]
}

resource "azurerm_container_app" "this" {
  name                         = var.name
  container_app_environment_id = azurerm_container_app_environment.this.id
  resource_group_name          = azurerm_resource_group.this.name
  revision_mode                = "Single"

  ingress {
    external_enabled           = true
    allow_insecure_connections = false
    target_port                = 80
    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  registry {
    identity = azurerm_user_assigned_identity.this[var.gh_repo].id
    server   = azurerm_container_registry.this.login_server
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.this[var.gh_repo].id]
  }

  template {
    container {
      name   = var.name
      image  = "${azurerm_container_registry.this.login_server}/${azurerm_container_registry_task.build_image[var.gh_repo].docker_step[0].image_names[0]}"
      cpu    = 1
      memory = "2Gi"

      env {
        name  = "IMAGES_URL_ROOT"
        value = "https://${azurerm_container_app.minio.ingress[0].fqdn}/pictograms/pictograms/"
      }
      env {
        name  = "CORE_URL"
        value = "https://${azurerm_container_app.core.ingress[0].fqdn}"
      }
    }
    min_replicas = var.scale.min
    max_replicas = var.scale.max
  }

  workload_profile_name = local.workload_profile_name

  depends_on = [
    azurerm_container_registry_task_schedule_run_now.build_image,
    azurerm_role_assignment.acr_pull,
  ]
}

# Patch Sticky sessions. This feature is still not available in the azurerm provider
# https://github.com/hashicorp/terraform-provider-azurerm/issues/24757#issuecomment-2213170796
resource "azapi_resource_action" "sticky_session" {
  type        = "Microsoft.App/containerApps@2024-03-01"
  resource_id = azurerm_container_app.this.id
  method      = "PATCH"
  body = {
    properties = {
      configuration = {
        ingress = {
          stickySessions = {
            affinity = "sticky"
          }
        }
      }
    }
  }

  depends_on = [azurerm_container_app.this]
}