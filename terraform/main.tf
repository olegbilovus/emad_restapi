terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.16.0"
    }
    azapi = {
      source  = "Azure/azapi"
      version = "2.2.0"
    }

    mongodbatlas = {
      source  = "mongodb/mongodbatlas"
      version = "1.26.0"
    }

    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "4.51.0"
    }
  }
}

provider "azurerm" {
  subscription_id = var.sub_id
  features {
  }
}

provider "azapi" {
}

provider "mongodbatlas" {
  public_key  = var.mongodb_pb_key
  private_key = var.mongodb_pv_key
}

provider "cloudflare" {
  api_key = var.cf_api_key
  email   = var.cf_email
}

resource "random_string" "random_suffix" {
  length  = 5
  special = false
  upper   = false
  keepers = {
    seed = 16754
  }
}

locals {
  rnd_str = random_string.random_suffix.result
  repos = {
    (var.gh_repo)       = replace(split("/", var.gh_repo)[4], "_", ""),
    (var.gh_minio_repo) = replace(split("/", var.gh_minio_repo)[4], "_", "")
    (var.gh_core_repo)  = replace(split("/", var.gh_core_repo)[4], "_", "")
  }
}

resource "azurerm_resource_group" "this" {
  name     = var.name
  location = var.location
}