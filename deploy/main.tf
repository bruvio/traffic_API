terraform {
  backend "s3" {
    bucket         = "bruvio-tfstate-traffic-app-api-ci"
    key            = "traffic-app.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-setup-tf-state-lock-traffic-app-api-ci"
  }
}

provider "aws" {
  region = "us-east-1"
}
locals {
  prefix = "${var.prefix}-${terraform.workspace}"
  common_tags = {
    Environment = terraform.workspace
    Project     = var.project
    Owner       = var.contact
    ManagedBy   = "Terraform"
  }


}

data "aws_region" "current" {}
