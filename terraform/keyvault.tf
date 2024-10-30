data "azurerm_client_config" "current" {}

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
    default_action             = "Allow"
    virtual_network_subnet_ids = [azurerm_subnet.container.id]
  }
}

resource "azurerm_role_assignment" "me" {
  scope                = azurerm_key_vault.this.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = data.azurerm_client_config.current.object_id
}

locals {
  secK_gh_access_token = "gh-access-token"
}

resource "azurerm_key_vault_secret" "this" {
  for_each = {
    # at the time of writing, ghcr does not support fine-grained tokens. Only the classic ones
    (local.secK_gh_access_token) = var.gh_access_token
  }

  name         = each.key
  value        = each.value
  key_vault_id = azurerm_key_vault.this.id

  depends_on = [azurerm_role_assignment.me]
}

resource "azurerm_user_assigned_identity" "this" {
  for_each = local.repos

  name                = each.value
  location            = var.location
  resource_group_name = azurerm_resource_group.this.name
}

resource "azurerm_role_assignment" "minio_secrets" {
  for_each = toset([
    local.secK_gh_access_token
  ])

  scope                = azurerm_key_vault_secret.this[each.key].resource_versionless_id
  role_definition_name = "Key Vault Secrets User"
  principal_id         = azurerm_user_assigned_identity.this[var.gh_minio_repo].principal_id
}