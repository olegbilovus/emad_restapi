resource "azurerm_cognitive_account" "openai" {
  name                          = "dalle3${local.rnd_str}"
  location                      = var.dalle3_location
  resource_group_name           = azurerm_resource_group.this.name
  kind                          = "OpenAI"
  sku_name                      = "S0"
  public_network_access_enabled = true
  local_auth_enabled            = true
}

resource "azurerm_cognitive_account_rai_policy" "noblock" {
  name                 = "noblock"
  cognitive_account_id = azurerm_cognitive_account.openai.id
  base_policy_name     = "Microsoft.Default"
  mode                 = "Default"

  dynamic "content_filter" {
    for_each = toset(["hate", "sexual", "selfharm", "violence", "jailbreak"])

    content {
      name               = content_filter.key
      filter_enabled     = true
      block_enabled      = true
      severity_threshold = "High"
      source             = "Prompt"
    }
  }

  dynamic "content_filter" {
    for_each = toset(["hate", "sexual", "selfharm", "violence", "protected_material_text", "protected_material_code"])

    content {
      name               = content_filter.key
      filter_enabled     = true
      block_enabled      = true
      severity_threshold = "High"
      source             = "Completion"
    }
  }

}

resource "azurerm_cognitive_deployment" "dalle3" {
  name                 = azurerm_cognitive_account.openai.name
  cognitive_account_id = azurerm_cognitive_account.openai.id
  rai_policy_name      = azurerm_cognitive_account_rai_policy.noblock.name

  model {
    format  = "OpenAI"
    name    = "dall-e-3"
    version = "3.0"
  }

  sku {
    name     = "Standard"
    capacity = 1
  }
}

