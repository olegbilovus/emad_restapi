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

variable "gh_access_token" {
  type      = string
  sensitive = true
  default   = "At the time of writing, ghcr does not support fine-grained tokens to. Only the classic ones"
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