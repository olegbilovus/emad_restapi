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
  default   = "At the time of writing, ghcr does not support fine-grained tokens. Only the classic ones"
}

variable "workload_profile_max" {
  default = 1
}