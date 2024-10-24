output "ACR_FQDN" {
  value = azurerm_container_registry.this.login_server
}

output "REST-API_FQDN" {
  value = azurerm_container_app.this.ingress[0].fqdn
}

output "MINIO-PICTOGRAMS_FQDN" {
  value = azurerm_container_app.minio.ingress[0].fqdn
}

output "GH-PAGES_URL" {
  value = github_repository.backend_url.pages[0].html_url
}