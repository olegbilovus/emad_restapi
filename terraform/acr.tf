resource "azurerm_container_registry" "this" {
  name                = "${var.name}${local.rnd_str}cr"
  resource_group_name = azurerm_resource_group.this.name
  location            = var.location
  sku                 = "Standard"
  admin_enabled       = true
}

# ACR Task to build and push the image to ACR
resource "azurerm_container_registry_task" "build_image" {
  name                  = "${var.name}buildimage"
  container_registry_id = azurerm_container_registry.this.id
  platform {
    os           = "Linux"
    architecture = "amd64"
  }
  source_trigger {
    name           = "buildoncommitmain"
    source_type    = "Github"
    events         = ["commit"]
    repository_url = var.gh_repo
    branch         = "main"
    authentication {
      token      = var.gh_access_token
      token_type = "PAT"
    }
  }
  docker_step {
    dockerfile_path      = "Dockerfile"
    context_path         = var.gh_repo
    context_access_token = var.gh_access_token
    image_names          = ["${var.name}:latest"]
  }
}

# Run the task, it will run only once even after doing another appy
resource "azurerm_container_registry_task_schedule_run_now" "build_image" {
  container_registry_task_id = azurerm_container_registry_task.build_image.id
}