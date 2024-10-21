data "azurerm_client_config" "current" {}

data "http" "myip" {
  url = "https://api.ipify.org/?format=text"
}

resource "azurerm_key_vault" "this" {
  name                       = "${var.name}-${local.rnd_str}-vault"
  location                   = var.location
  resource_group_name        = azurerm_resource_group.this.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  soft_delete_retention_days = 7
  purge_protection_enabled   = false
  enable_rbac_authorization  = true
  sku_name                   = "standard"

  network_acls {
    bypass                     = "AzureServices"
    default_action             = "Deny"
    virtual_network_subnet_ids = [azurerm_subnet.container.id]
    ip_rules                   = [chomp(data.http.myip.response_body)]
  }
}

resource "azurerm_role_assignment" "this" {
  scope                = azurerm_key_vault.this.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_key_vault_secret" "apirest" {
  for_each = {
    jwt-secret = var.JWT_SECRET
  }
  name         = each.key
  value        = each.value
  key_vault_id = azurerm_key_vault.this.id

  depends_on = [azurerm_role_assignment.this]
}

resource "azurerm_role_assignment" "apirest_secrets" {
  for_each = toset([
    "jwt-secret"
  ])

  scope                = azurerm_key_vault_secret.apirest[each.key].resource_versionless_id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_user_assigned_identity.this.principal_id
}
