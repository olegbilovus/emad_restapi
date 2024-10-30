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

resource "azurerm_container_registry_task" "this" {
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
    image_names          = ["${local.repos[var.gh_repo]}:latest"]
  }
}

resource "azurerm_container_registry_task" "core" {
  for_each = {
    it = {
      args : {
        "SPACY_MODEL" : "it_core_news_lg"
      }
    },
    en = {
      args : {
        "SPACY_MODEL" : "en_core_web_lg"
      }
    }
  }
  name                  = "${local.repos[var.gh_core_repo]}${each.key}buildimage"
  container_registry_id = azurerm_container_registry.this.id
  platform {
    os           = "Linux"
    architecture = "amd64"
  }
  source_trigger {
    name           = "buildoncommitmain"
    source_type    = "Github"
    events         = ["commit"]
    repository_url = var.gh_core_repo
    branch         = "main"
    authentication {
      token      = var.gh_access_token
      token_type = "PAT"
    }
  }
  docker_step {
    dockerfile_path      = "Dockerfile"
    context_path         = var.gh_core_repo
    context_access_token = var.gh_access_token
    image_names          = ["${local.repos[var.gh_core_repo]}:${each.key}"]
    arguments            = each.value["args"]
  }
}

# Run the tasks to build the images, it will run only once even after doing another appy
resource "azurerm_container_registry_task_schedule_run_now" "this" {
  container_registry_task_id = azurerm_container_registry_task.this.id
}

resource "azurerm_container_registry_task_schedule_run_now" "core" {
  for_each = azurerm_container_registry_task.core


  container_registry_task_id = each.value.id
}