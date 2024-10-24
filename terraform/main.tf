terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.6.0"
    }
    azapi = {
      source  = "Azure/azapi"
      version = "2.0.0-beta"
    }

    github = {
      source  = "integrations/github"
      version = "6.3.1"
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
  }
}

resource "azurerm_resource_group" "this" {
  name     = var.name
  location = var.location
}