output "ACR_FQDN" {
  value = azurerm_container_registry.this.login_server
}