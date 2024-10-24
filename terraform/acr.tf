resource "azurerm_container_registry" "this" {
  name                = "${var.name}${local.rnd_str}cr"
  resource_group_name = azurerm_resource_group.this.name
  location            = var.location
  sku                 = "Standard"
  admin_enabled       = true
}

# RBAC for ACR Pull
resource "azurerm_role_assignment" "acr_pull" {
  for_each = azurerm_user_assigned_identity.this

  scope                = azurerm_container_registry.this.id
  role_definition_name = "AcrPull"
  principal_id         = each.value.principal_id
}

# ACR Task to build and push the images to ACR
resource "azurerm_container_registry_task" "build_image" {
  for_each = local.repos

  name                  = "${each.value}buildimage"
  container_registry_id = azurerm_container_registry.this.id
  platform {
    os           = "Linux"
    architecture = "amd64"
  }
  source_trigger {
    name           = "buildoncommitmain"
    source_type    = "Github"
    events         = ["commit"]
    repository_url = each.key
    branch         = "main"
    authentication {
      token      = var.gh_access_token
      token_type = "PAT"
    }
  }
  docker_step {
    dockerfile_path      = "Dockerfile"
    context_path         = each.key
    context_access_token = var.gh_access_token
    image_names          = ["${each.value}:latest"]
  }
}

# Run the tasks to build the images, it will run only once even after doing another appy
resource "azurerm_container_registry_task_schedule_run_now" "build_image" {
  for_each = azurerm_container_registry_task.build_image

  container_registry_task_id = each.value.id
}