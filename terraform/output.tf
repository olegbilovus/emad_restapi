output "REST-API_FQDN" {
  value = [
    azurerm_container_app.this.ingress[0].fqdn,
    azurerm_container_app_custom_domain.this["api"].name
  ]
}

output "MINIO-PICTOGRAMS_FQDN" {
  value = [
    azurerm_container_app.minio.ingress[0].fqdn,
    azurerm_container_app_custom_domain.this["images"].name
  ]
}

output "MONGO_DB-CONN_STR" {
  value = local.mongodb_url
}