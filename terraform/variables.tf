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
  type      = string
  sensitive = true
}

variable "gh_access_token" {
  type      = string
  sensitive = true
}

variable "workload_profile_max" {
  default = 1
}

variable "my_ip" {
  type      = string
  sensitive = true
}

variable "JWT_SECRET" {
  type      = string
  sensitive = true
}

variable "ACCESS_TOKEN_EXPIRE_MINUTES" {
  type = number
}