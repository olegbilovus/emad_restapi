variable "sub_id" {
  type      = string
  sensitive = true
}

variable "name" {
  default = "emadrestapi"
}

variable "location" {
  default = "francecentral"
}

variable "gh_repo" {
  type = string
}

variable "gh_minio_repo" {
  type = string
}

variable "gh_access_token" {
  type      = string
  sensitive = true
}

variable "workload_profile_max" {
  default = 1
}