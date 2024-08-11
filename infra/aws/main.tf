terraform {
  backend "remote" {
    organization = "PSIOG"
    workspaces{
      name="tutorial"
    }
  }
  
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
  bucket = var.aws_s3_bucket

  tags = {
    Name        = "My test-bucket"
    Environment = "Dev"
  }
}