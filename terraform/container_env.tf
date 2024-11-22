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
  ghcr = {
    server               = "ghcr.io"
    username             = split("/", var.gh_minio_repo)[3]
    password_secret_name = "gh-access-token"
  }
}


resource "azurerm_container_app" "core" {
  for_each = toset(["it", "en"])

  name                         = "core${each.key}"
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
    server               = local.ghcr.server
    username             = local.ghcr.username
    password_secret_name = local.ghcr.password_secret_name
  }

  secret {
    name  = local.ghcr.password_secret_name
    value = var.gh_access_token
  }

  template {
    container {
      name   = "core${each.key}"
      image  = "ghcr.io/${local.ghcr.username}/${split("/", var.gh_core_repo)[4]}:${each.key}"
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
      env {
        name  = "JSON_FILE"
        value = "jsons/${each.key}.json"
      }
      env {
        name  = "LANGUAGE"
        value = each.key
      }
    }
    min_replicas = var.scale.min
    max_replicas = var.scale.max
  }

  workload_profile_name = local.workload_profile_name

  depends_on = [
    mongodbatlas_database_user.admin,
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

  registry {
    server               = local.ghcr.server
    username             = local.ghcr.username
    password_secret_name = local.ghcr.password_secret_name
  }

  secret {
    name  = local.ghcr.password_secret_name
    value = var.gh_access_token
  }

  template {
    container {
      name   = local.repos[var.gh_minio_repo]
      image  = "ghcr.io/${local.ghcr.username}/${split("/", var.gh_minio_repo)[4]}:latest"
      cpu    = 1
      memory = "2Gi"
    }
    min_replicas = var.scale.min
    max_replicas = var.scale.max
  }

  workload_profile_name = local.workload_profile_name
}

resource "azurerm_container_app" "this" {
  name                         = local.repos[var.gh_repo]
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
    server               = local.ghcr.server
    username             = local.ghcr.username
    password_secret_name = local.ghcr.password_secret_name
  }

  secret {
    name  = local.ghcr.password_secret_name
    value = var.gh_access_token
  }

  template {
    container {
      name   = local.repos[var.gh_repo]
      image  = "ghcr.io/${local.ghcr.username}/${split("/", var.gh_repo)[4]}:latest"
      cpu    = 1
      memory = "2Gi"

      env {
        name  = "APP_ENV"
        value = "azure"
      }
      env {
        name  = "IMAGES_URL_ROOT"
        value = "https://${azurerm_container_app.minio.ingress[0].fqdn}/pictograms/pictograms/"
      }
      env {
        name  = "CORE_URL_IT"
        value = "https://${azurerm_container_app.core["it"].ingress[0].fqdn}"
      }
      env {
        name  = "CORE_URL_EN"
        value = "https://${azurerm_container_app.core["en"].ingress[0].fqdn}"
      }
      env {
        name  = "DALLE3_ENDPOINT"
        value = "${azurerm_cognitive_account.openai.endpoint}openai/deployments/${azurerm_cognitive_deployment.dalle3.name}/images/generations?api-version=2024-06-01"
      }
      env {
        name  = "DALLE3_APIKEY"
        value = azurerm_cognitive_account.openai.primary_access_key
      }
      env {
        name  = "CLIENT_APIKEY"
        value = var.client_apikey
      }
      dynamic "env" {
        for_each = var.influxdb
        content {
          name  = upper("INFLUXDB_${env.key}")
          value = env.value
        }
      }
    }
    min_replicas = var.scale.min
    max_replicas = var.scale.max
  }

  workload_profile_name = local.workload_profile_name
}

resource "null_resource" "wait_for_dns_propagation" {
  provisioner "local-exec" {
    command = "sleep 60"
  }

  depends_on = [
    cloudflare_record.azure_verify_images,
    cloudflare_record.azure_verify_this,
    cloudflare_record.this
  ]
}

resource "azurerm_container_app_custom_domain" "this" {
  for_each = {
    images = azurerm_container_app.minio.id
    api    = azurerm_container_app.this.id
  }

  name             = "${each.key}.${var.cf_domain}"
  container_app_id = each.value

  lifecycle {
    // When using an Azure created Managed Certificate these values must be added to ignore_changes to prevent resource recreation.
    ignore_changes = [certificate_binding_type, container_app_environment_certificate_id]
  }

  depends_on = [
    cloudflare_record.azure_verify_images,
    cloudflare_record.azure_verify_this,
    null_resource.wait_for_dns_propagation
  ]
}

# https://github.com/hashicorp/terraform-provider-azurerm/issues/27362
resource "null_resource" "custom_domain_and_managed_certificate" {
  for_each = {
    images = azurerm_container_app.minio.name
    api    = azurerm_container_app.this.name
  }

  provisioner "local-exec" {
    command = "az containerapp hostname bind --hostname ${each.key}.${var.cf_domain} -g ${azurerm_resource_group.this.name} -n ${each.value} --environment ${azurerm_container_app_environment.this.name} --validation-method CNAME"
  }
  triggers = local.cf_subdomains
  depends_on = [
    azurerm_container_app_custom_domain.this,
    null_resource.wait_for_dns_propagation
  ]
}