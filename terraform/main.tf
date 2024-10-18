terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.6.0"
    }
  }
}

provider "azurerm" {
  subscription_id = var.sub_id
  features {
  }
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
}

resource "azurerm_resource_group" "this" {
  name     = var.name
  location = var.location
}