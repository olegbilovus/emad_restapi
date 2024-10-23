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

resource "azurerm_user_assigned_identity" "this" {
  for_each = local.repos

  name                = each.value
  location            = var.location
  resource_group_name = azurerm_resource_group.this.name
}

# RBAC for ACR Pull
resource "azurerm_role_assignment" "acr_pull" {
  for_each = azurerm_user_assigned_identity.this

  scope                = azurerm_container_registry.this.id
  role_definition_name = "AcrPull"
  principal_id         = each.value.principal_id
}

resource "azurerm_container_app" "this" {
  name                         = var.name
  container_app_environment_id = azurerm_container_app_environment.this.id
  resource_group_name          = azurerm_resource_group.this.name
  revision_mode                = "Single"

  ingress {
    external_enabled           = true
    allow_insecure_connections = true
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
    }
    max_replicas = var.workload_profile_max
    min_replicas = 1
  }

  workload_profile_name = local.workload_profile_name

  depends_on = [
    azurerm_container_registry_task_schedule_run_now.build_image,
    azurerm_role_assignment.acr_pull
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

  template {
    container {
      name   = local.repos[var.gh_minio_repo]
      image  = "ghcr.io/${split("/", var.gh_minio_repo)[3]}/${split("/", var.gh_minio_repo)[4]}:latest"
      cpu    = 1
      memory = "2Gi"
    }
    max_replicas = var.workload_profile_max
    min_replicas = 1
  }

  workload_profile_name = local.workload_profile_name

  depends_on = [
    azurerm_container_registry_task_schedule_run_now.build_image,
    azurerm_role_assignment.acr_pull
  ]
}