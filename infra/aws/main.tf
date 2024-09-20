terraform {
  backend "remote" {
    organization = "PSIOG"
    workspaces {
      name = "tutorial"
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

provider "random" {

}

resource "random_pet" "name" {

}

# resource "aws_s3_bucket" "example" {
#   bucket = var.aws_s3_bucket

#   tags = {
#     Name        = "My test-bucket"
#     Environment = "Dev"
#   }
# }

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "webserver" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t1.micro"
  user_data     = file("init-script.sh")

  tags = {
    Name = random_pet.name.id
  }
}

