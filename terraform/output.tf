output "ACR_FQDN" {
  value = azurerm_container_registry.this.login_server
}

output "REST-API_FQDN" {
  value = azurerm_container_app.this.ingress[0].fqdn
}

output "MINIO-PICTOGRAMS_FQDN" {
  value = azurerm_container_app.minio.ingress[0].fqdn
}