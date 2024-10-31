resource "azurerm_cognitive_account" "openai" {
  name                          = "dalle3${local.rnd_str}"
  location                      = var.dalle3_location
  resource_group_name           = azurerm_resource_group.this.name
  kind                          = "OpenAI"
  sku_name                      = "S0"
  public_network_access_enabled = true
}

resource "azapi_resource" "content_filter" {
  type      = "Microsoft.CognitiveServices/accounts/raiPolicies@2024-10-01"
  name      = "noblock"
  parent_id = azurerm_cognitive_account.openai.id

  schema_validation_enabled = false

  body = {
    properties = {
      mode           = "Default",
      basePolicyName = "Microsoft.Default",
      contentFilters = [
        { name = "hate", blocking = true, enabled = true, severityThreshold = "High", source = "Prompt" },
        { name = "sexual", blocking = true, enabled = true, severityThreshold = "High", source = "Prompt" },
        { name = "selfharm", blocking = true, enabled = true, severityThreshold = "High", source = "Prompt" },
        { name = "violence", blocking = true, enabled = true, severityThreshold = "High", source = "Prompt" },
        { name = "hate", blocking = true, enabled = true, severityThreshold = "High", source = "Completion" },
        { name = "sexual", blocking = true, enabled = true, severityThreshold = "High", source = "Completion" },
        { name = "selfharm", blocking = true, enabled = true, severityThreshold = "High", source = "Completion" },
        { name = "violence", blocking = true, enabled = true, severityThreshold = "High", source = "Completion" },
        { name = "jailbreak", blocking = true, enabled = true, source = "Prompt" },
        { name = "protected_material_text", blocking = true, enabled = true, source = "Completion" },
        { name = "protected_material_code", blocking = true, enabled = true, source = "Completion" }
      ]
    }
  }

  depends_on = [azurerm_cognitive_account.openai]
  lifecycle {
    ignore_changes = [
      body
    ]
  }
}

resource "azurerm_cognitive_deployment" "dalle3" {
  name                 = azurerm_cognitive_account.openai.name
  cognitive_account_id = azurerm_cognitive_account.openai.id
  rai_policy_name      = azapi_resource.content_filter.name

  model {
    format  = "OpenAI"
    name    = "dall-e-3"
    version = "3.0"
  }

  sku {
    name     = "Standard"
    capacity = 1
  }

  depends_on = [azapi_resource.content_filter]
}

