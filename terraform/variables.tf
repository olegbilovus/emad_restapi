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

