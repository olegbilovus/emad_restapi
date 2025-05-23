<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_azurerm"></a> [azurerm](#requirement\_azurerm) | 4.18.0 |
| <a name="requirement_cloudflare"></a> [cloudflare](#requirement\_cloudflare) | 4.52.0 |
| <a name="requirement_mongodbatlas"></a> [mongodbatlas](#requirement\_mongodbatlas) | 1.26.1 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_azurerm"></a> [azurerm](#provider\_azurerm) | 4.18.0 |
| <a name="provider_cloudflare"></a> [cloudflare](#provider\_cloudflare) | 4.52.0 |
| <a name="provider_mongodbatlas"></a> [mongodbatlas](#provider\_mongodbatlas) | 1.26.1 |
| <a name="provider_null"></a> [null](#provider\_null) | n/a |
| <a name="provider_random"></a> [random](#provider\_random) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [azurerm_cognitive_account.openai](https://registry.terraform.io/providers/hashicorp/azurerm/4.18.0/docs/resources/cognitive_account) | resource |
| [azurerm_cognitive_account_rai_policy.noblock](https://registry.terraform.io/providers/hashicorp/azurerm/4.18.0/docs/resources/cognitive_account_rai_policy) | resource |
| [azurerm_cognitive_deployment.dalle3](https://registry.terraform.io/providers/hashicorp/azurerm/4.18.0/docs/resources/cognitive_deployment) | resource |
| [azurerm_container_app.core](https://registry.terraform.io/providers/hashicorp/azurerm/4.18.0/docs/resources/container_app) | resource |
| [azurerm_container_app.minio](https://registry.terraform.io/providers/hashicorp/azurerm/4.18.0/docs/resources/container_app) | resource |
| [azurerm_container_app.this](https://registry.terraform.io/providers/hashicorp/azurerm/4.18.0/docs/resources/container_app) | resource |
| [azurerm_container_app_custom_domain.this](https://registry.terraform.io/providers/hashicorp/azurerm/4.18.0/docs/resources/container_app_custom_domain) | resource |
| [azurerm_container_app_environment.this](https://registry.terraform.io/providers/hashicorp/azurerm/4.18.0/docs/resources/container_app_environment) | resource |
| [azurerm_resource_group.this](https://registry.terraform.io/providers/hashicorp/azurerm/4.18.0/docs/resources/resource_group) | resource |
| [azurerm_subnet.container](https://registry.terraform.io/providers/hashicorp/azurerm/4.18.0/docs/resources/subnet) | resource |
| [azurerm_virtual_network.container_env](https://registry.terraform.io/providers/hashicorp/azurerm/4.18.0/docs/resources/virtual_network) | resource |
| [cloudflare_record.azure_verify_images](https://registry.terraform.io/providers/cloudflare/cloudflare/4.52.0/docs/resources/record) | resource |
| [cloudflare_record.azure_verify_this](https://registry.terraform.io/providers/cloudflare/cloudflare/4.52.0/docs/resources/record) | resource |
| [cloudflare_record.this](https://registry.terraform.io/providers/cloudflare/cloudflare/4.52.0/docs/resources/record) | resource |
| [mongodbatlas_advanced_cluster.this](https://registry.terraform.io/providers/mongodb/mongodbatlas/1.26.1/docs/resources/advanced_cluster) | resource |
| [mongodbatlas_database_user.admin](https://registry.terraform.io/providers/mongodb/mongodbatlas/1.26.1/docs/resources/database_user) | resource |
| [mongodbatlas_database_user.core](https://registry.terraform.io/providers/mongodb/mongodbatlas/1.26.1/docs/resources/database_user) | resource |
| [mongodbatlas_project_ip_access_list.anyone](https://registry.terraform.io/providers/mongodb/mongodbatlas/1.26.1/docs/resources/project_ip_access_list) | resource |
| [null_resource.custom_domain_and_managed_certificate](https://registry.terraform.io/providers/hashicorp/null/latest/docs/resources/resource) | resource |
| [null_resource.wait_for_dns_propagation](https://registry.terraform.io/providers/hashicorp/null/latest/docs/resources/resource) | resource |
| [random_string.random_suffix](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/string) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_cf_api_key"></a> [cf\_api\_key](#input\_cf\_api\_key) | n/a | `string` | n/a | yes |
| <a name="input_cf_domain"></a> [cf\_domain](#input\_cf\_domain) | n/a | `string` | n/a | yes |
| <a name="input_cf_email"></a> [cf\_email](#input\_cf\_email) | n/a | `string` | n/a | yes |
| <a name="input_cf_zone_id"></a> [cf\_zone\_id](#input\_cf\_zone\_id) | n/a | `string` | n/a | yes |
| <a name="input_client_apikey"></a> [client\_apikey](#input\_client\_apikey) | n/a | `string` | n/a | yes |
| <a name="input_dalle3_location"></a> [dalle3\_location](#input\_dalle3\_location) | n/a | `string` | `"swedencentral"` | no |
| <a name="input_gh_access_token"></a> [gh\_access\_token](#input\_gh\_access\_token) | At the time of writing, ghcr does not support fine-grained tokens to. Only the classic ones | `string` | n/a | yes |
| <a name="input_gh_core_repo"></a> [gh\_core\_repo](#input\_gh\_core\_repo) | n/a | `string` | n/a | yes |
| <a name="input_gh_minio_repo"></a> [gh\_minio\_repo](#input\_gh\_minio\_repo) | n/a | `string` | n/a | yes |
| <a name="input_gh_repo"></a> [gh\_repo](#input\_gh\_repo) | n/a | `string` | n/a | yes |
| <a name="input_googleai"></a> [googleai](#input\_googleai) | n/a | <pre>object({<br/>    api_key = string<br/>    model   = string<br/>  })</pre> | n/a | yes |
| <a name="input_influxdb"></a> [influxdb](#input\_influxdb) | n/a | <pre>object({<br/>    url    = string<br/>    token  = string<br/>    org    = string<br/>    bucket = string<br/>  })</pre> | n/a | yes |
| <a name="input_location"></a> [location](#input\_location) | n/a | `string` | `"westeurope"` | no |
| <a name="input_mongodb_pb_key"></a> [mongodb\_pb\_key](#input\_mongodb\_pb\_key) | n/a | `string` | n/a | yes |
| <a name="input_mongodb_project_id"></a> [mongodb\_project\_id](#input\_mongodb\_project\_id) | n/a | `string` | n/a | yes |
| <a name="input_mongodb_pv_key"></a> [mongodb\_pv\_key](#input\_mongodb\_pv\_key) | n/a | `string` | n/a | yes |
| <a name="input_mongodb_user_admin"></a> [mongodb\_user\_admin](#input\_mongodb\_user\_admin) | n/a | <pre>object({<br/>    username = string<br/>    password = string<br/>  })</pre> | n/a | yes |
| <a name="input_mongodb_user_core"></a> [mongodb\_user\_core](#input\_mongodb\_user\_core) | n/a | <pre>object({<br/>    username = string<br/>    password = string<br/>  })</pre> | n/a | yes |
| <a name="input_name"></a> [name](#input\_name) | n/a | `string` | `"emadrestapi"` | no |
| <a name="input_openai"></a> [openai](#input\_openai) | n/a | <pre>object({<br/>    base_url           = string<br/>    api_key            = string<br/>    model              = string<br/>    force_fix_sentence = bool<br/>  })</pre> | n/a | yes |
| <a name="input_scale"></a> [scale](#input\_scale) | n/a | <pre>object({<br/>    min = number,<br/>    max = number<br/>  })</pre> | <pre>{<br/>  "max": 1,<br/>  "min": 1<br/>}</pre> | no |
| <a name="input_sub_id"></a> [sub\_id](#input\_sub\_id) | n/a | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_MINIO-PICTOGRAMS_FQDN"></a> [MINIO-PICTOGRAMS\_FQDN](#output\_MINIO-PICTOGRAMS\_FQDN) | n/a |
| <a name="output_MONGO_DB-CONN_STR"></a> [MONGO\_DB-CONN\_STR](#output\_MONGO\_DB-CONN\_STR) | n/a |
| <a name="output_REST-API_FQDN"></a> [REST-API\_FQDN](#output\_REST-API\_FQDN) | n/a |
<!-- END_TF_DOCS -->