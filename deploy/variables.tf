variable "prefix" {
  default = "raad"
}
variable "project" {
  default = "traffic-Django-restAPI-AWS"
}

variable "contact" {
  default = "bruno.viola@pm.me"
}
variable "db_username" {
  description = "username for RDS postgrase database"
}
variable "db_password" {
  description = "password for RDS postgrase database"
}
variable "bastion_key_name" {
  default = "traffic-app-api-devops-bastion"
}

variable "ecr_image_api" {
  description = "ECR Image for API"
  default     = "546123287190.dkr.ecr.us-east-1.amazonaws.com/traffic-django-restapi-app:latest"
}

variable "ecr_image_proxy" {
  description = "ECR Image for API"
  default     = "546123287190.dkr.ecr.us-east-1.amazonaws.com/traffic-django-restapi-proxy:latest"
}

variable "django_secret_key" {
  description = "Secret key for Django app"
}
variable "admin" {
  description = "admin name"
}
variable "admin_email" {
  description = "Admin email"
}
variable "admin_password" {
  description = "password for admin"
}

variable "dns_zone_name" {
  description = "Domain name"
  default     = "brunoviola.net"
}

variable "subdomain" {
  description = "Subdomain per environment"
  type        = map(string)
  default = {
    production = "api"
    staging    = "api.staging"
    dev        = "api.dev"
  }
}
