terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "example" {
  bucket = "${var.aws_s3_bucket}"

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}

variable "aws_s3_bucket" {
  default     = "2432432jnjn23432j234"
  description = "S3 bucket used for file batch job resources"
}