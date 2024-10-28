<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_azapi"></a> [azapi](#requirement\_azapi) | 2.0.0-beta |
| <a name="requirement_azurerm"></a> [azurerm](#requirement\_azurerm) | 4.6.0 |
| <a name="requirement_github"></a> [github](#requirement\_github) | 6.3.1 |
| <a name="requirement_mongodbatlas"></a> [mongodbatlas](#requirement\_mongodbatlas) | 1.21.3 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_azapi"></a> [azapi](#provider\_azapi) | 2.0.0-beta |
| <a name="provider_azurerm"></a> [azurerm](#provider\_azurerm) | 4.6.0 |
| <a name="provider_github"></a> [github](#provider\_github) | 6.3.1 |
| <a name="provider_http"></a> [http](#provider\_http) | n/a |
| <a name="provider_mongodbatlas"></a> [mongodbatlas](#provider\_mongodbatlas) | 1.21.3 |
| <a name="provider_random"></a> [random](#provider\_random) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [azapi_resource_action.sticky_session](https://registry.terraform.io/providers/Azure/azapi/2.0.0-beta/docs/resources/resource_action) | resource |
| [azurerm_container_app.core](https://registry.terraform.io/providers/hashicorp/azurerm/4.6.0/docs/resources/container_app) | resource |
| [azurerm_container_app.minio](https://registry.terraform.io/providers/hashicorp/azurerm/4.6.0/docs/resources/container_app) | resource |
| [azurerm_container_app.this](https://registry.terraform.io/providers/hashicorp/azurerm/4.6.0/docs/resources/container_app) | resource |
| [azurerm_container_app_environment.this](https://registry.terraform.io/providers/hashicorp/azurerm/4.6.0/docs/resources/container_app_environment) | resource |
| [azurerm_container_registry.this](https://registry.terraform.io/providers/hashicorp/azurerm/4.6.0/docs/resources/container_registry) | resource |
| [azurerm_container_registry_task.build_image](https://registry.terraform.io/providers/hashicorp/azurerm/4.6.0/docs/resources/container_registry_task) | resource |
| [azurerm_container_registry_task_schedule_run_now.build_image](https://registry.terraform.io/providers/hashicorp/azurerm/4.6.0/docs/resources/container_registry_task_schedule_run_now) | resource |
| [azurerm_key_vault.this](https://registry.terraform.io/providers/hashicorp/azurerm/4.6.0/docs/resources/key_vault) | resource |
| [azurerm_key_vault_secret.this](https://registry.terraform.io/providers/hashicorp/azurerm/4.6.0/docs/resources/key_vault_secret) | resource |
| [azurerm_resource_group.this](https://registry.terraform.io/providers/hashicorp/azurerm/4.6.0/docs/resources/resource_group) | resource |
| [azurerm_role_assignment.acr_pull](https://registry.terraform.io/providers/hashicorp/azurerm/4.6.0/docs/resources/role_assignment) | resource |
| [azurerm_role_assignment.me](https://registry.terraform.io/providers/hashicorp/azurerm/4.6.0/docs/resources/role_assignment) | resource |
| [azurerm_role_assignment.minio_secrets](https://registry.terraform.io/providers/hashicorp/azurerm/4.6.0/docs/resources/role_assignment) | resource |
| [azurerm_subnet.container](https://registry.terraform.io/providers/hashicorp/azurerm/4.6.0/docs/resources/subnet) | resource |
| [azurerm_user_assigned_identity.this](https://registry.terraform.io/providers/hashicorp/azurerm/4.6.0/docs/resources/user_assigned_identity) | resource |
| [azurerm_virtual_network.container_env](https://registry.terraform.io/providers/hashicorp/azurerm/4.6.0/docs/resources/virtual_network) | resource |
| [github_repository.backend_url](https://registry.terraform.io/providers/integrations/github/6.3.1/docs/resources/repository) | resource |
| [github_repository_file.backend_url](https://registry.terraform.io/providers/integrations/github/6.3.1/docs/resources/repository_file) | resource |
| [mongodbatlas_advanced_cluster.this](https://registry.terraform.io/providers/mongodb/mongodbatlas/1.21.3/docs/resources/advanced_cluster) | resource |
| [mongodbatlas_database_user.admin](https://registry.terraform.io/providers/mongodb/mongodbatlas/1.21.3/docs/resources/database_user) | resource |
| [mongodbatlas_database_user.core](https://registry.terraform.io/providers/mongodb/mongodbatlas/1.21.3/docs/resources/database_user) | resource |
| [mongodbatlas_project_ip_access_list.anyone](https://registry.terraform.io/providers/mongodb/mongodbatlas/1.21.3/docs/resources/project_ip_access_list) | resource |
| [random_string.random_suffix](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/string) | resource |
| [azurerm_client_config.current](https://registry.terraform.io/providers/hashicorp/azurerm/4.6.0/docs/data-sources/client_config) | data source |
| [http_http.myip](https://registry.terraform.io/providers/hashicorp/http/latest/docs/data-sources/http) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_gh_access_token"></a> [gh\_access\_token](#input\_gh\_access\_token) | At the time of writing, ghcr does not support fine-grained tokens to. Only the classic ones | `string` | n/a | yes |
| <a name="input_gh_core_repo"></a> [gh\_core\_repo](#input\_gh\_core\_repo) | n/a | `string` | n/a | yes |
| <a name="input_gh_minio_repo"></a> [gh\_minio\_repo](#input\_gh\_minio\_repo) | n/a | `string` | n/a | yes |
| <a name="input_gh_repo"></a> [gh\_repo](#input\_gh\_repo) | n/a | `string` | n/a | yes |
| <a name="input_location"></a> [location](#input\_location) | n/a | `string` | `"westeurope"` | no |
| <a name="input_mongodb_pb_key"></a> [mongodb\_pb\_key](#input\_mongodb\_pb\_key) | n/a | `string` | n/a | yes |
| <a name="input_mongodb_project_id"></a> [mongodb\_project\_id](#input\_mongodb\_project\_id) | n/a | `string` | n/a | yes |
| <a name="input_mongodb_pv_key"></a> [mongodb\_pv\_key](#input\_mongodb\_pv\_key) | n/a | `string` | n/a | yes |
| <a name="input_mongodb_user_admin"></a> [mongodb\_user\_admin](#input\_mongodb\_user\_admin) | n/a | <pre>object({<br/>    username = string<br/>    password = string<br/>  })</pre> | n/a | yes |
| <a name="input_mongodb_user_core"></a> [mongodb\_user\_core](#input\_mongodb\_user\_core) | n/a | <pre>object({<br/>    username = string<br/>    password = string<br/>  })</pre> | n/a | yes |
| <a name="input_name"></a> [name](#input\_name) | n/a | `string` | `"emadrestapi"` | no |
| <a name="input_scale"></a> [scale](#input\_scale) | n/a | <pre>object({<br/>    min = number,<br/>    max = number<br/>  })</pre> | <pre>{<br/>  "max": 1,<br/>  "min": 1<br/>}</pre> | no |
| <a name="input_sub_id"></a> [sub\_id](#input\_sub\_id) | n/a | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_ACR_FQDN"></a> [ACR\_FQDN](#output\_ACR\_FQDN) | n/a |
| <a name="output_GH-PAGES_URL"></a> [GH-PAGES\_URL](#output\_GH-PAGES\_URL) | n/a |
| <a name="output_MINIO-PICTOGRAMS_FQDN"></a> [MINIO-PICTOGRAMS\_FQDN](#output\_MINIO-PICTOGRAMS\_FQDN) | n/a |
| <a name="output_MONGO_DB-CONN_STR"></a> [MONGO\_DB-CONN\_STR](#output\_MONGO\_DB-CONN\_STR) | n/a |
| <a name="output_REST-API_FQDN"></a> [REST-API\_FQDN](#output\_REST-API\_FQDN) | n/a |
<!-- END_TF_DOCS -->