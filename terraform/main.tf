terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.10.0"
    }
    azapi = {
      source  = "Azure/azapi"
      version = "2.0.1"
    }

    github = {
      source  = "integrations/github"
      version = "6.3.1"
    }

    mongodbatlas = {
      source  = "mongodb/mongodbatlas"
      version = "1.21.4"
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

provider "github" {
  token = var.gh_access_token
  owner = local.gh_username
}

provider "mongodbatlas" {
  public_key  = var.mongodb_pb_key
  private_key = var.mongodb_pv_key
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