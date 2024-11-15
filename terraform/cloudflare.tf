locals {
  cf_subdomains = {
    images = azurerm_container_app.minio.ingress[0].fqdn
    api    = azurerm_container_app.this.ingress[0].fqdn
  }
}

resource "cloudflare_record" "azure_verify_this" {
  name    = "asuid.api"
  proxied = false
  ttl     = 1
  type    = "TXT"
  content = "\"${azurerm_container_app.this.custom_domain_verification_id}\""
  zone_id = var.cf_zone_id

  lifecycle {
    replace_triggered_by = [azurerm_container_app.this]
  }
}

resource "cloudflare_record" "azure_verify_images" {
  name    = "asuid.images"
  proxied = false
  ttl     = 1
  type    = "TXT"
  content = "\"${azurerm_container_app.minio.custom_domain_verification_id}\""
  zone_id = var.cf_zone_id

  lifecycle {
    replace_triggered_by = [azurerm_container_app.minio]
  }
}

resource "cloudflare_record" "this" {
  for_each = local.cf_subdomains

  name    = "${each.key}.${var.cf_domain}"
  proxied = false
  ttl     = 1
  type    = "CNAME"
  content = each.value
  zone_id = var.cf_zone_id

  lifecycle {
    replace_triggered_by = [
      azurerm_container_app.minio,
      azurerm_container_app.this
    ]
  }
}