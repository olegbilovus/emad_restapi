variable "sub_id" {
  type      = string
  sensitive = true
}

variable "name" {
  default = "emadrestapi"
}

variable "location" {
  default = "westeurope"
}

variable "gh_repo" {
  type = string
}

variable "gh_minio_repo" {
  type = string
}

variable "gh_core_repo" {
  type = string
}

variable "gh_access_token" {
  type        = string
  sensitive   = true
  description = "At the time of writing, ghcr does not support fine-grained tokens to. Only the classic ones"
}

variable "scale" {
  type = object({
    min = number,
    max = number
  })

  default = {
    min = 1
    max = 1
  }

  validation {
    condition     = var.scale.min <= var.scale.max && var.scale.min >= 0
    error_message = "Invalid min or max"
  }
}

variable "mongodb_pb_key" {
  type      = string
  sensitive = true
}

variable "mongodb_pv_key" {
  type      = string
  sensitive = true
}

variable "mongodb_project_id" {
  type      = string
  sensitive = true
}

variable "mongodb_user_admin" {
  type = object({
    username = string
    password = string
  })

  sensitive = true
}

variable "mongodb_user_core" {
  type = object({
    username = string
    password = string
  })

  sensitive = true
}

variable "dalle3_location" {
  default = "swedencentral"
}

variable "client_apikey" {
  type      = string
  sensitive = true
}

variable "cf_api_key" {
  type      = string
  sensitive = true
}

variable "cf_email" {
  type      = string
  sensitive = true
}

variable "cf_zone_id" {
  type      = string
  sensitive = true
}

variable "cf_domain" {
  type = string
}

variable "influxdb" {
  type = object({
    url    = string
    token  = string
    org    = string
    bucket = string
  })
}
