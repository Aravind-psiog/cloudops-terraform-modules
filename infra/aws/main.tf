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

resource "aws_s3_bucket" "example" {
  bucket = var.aws_s3_bucket

  tags = {
    Name        = "My test-bucket"
    Environment = "Dev"
  }
}

data "aws_ami" "ubuntu-linux-1404" {
  most_recent = true
  owners      = ["099720109477"] # Canonical
  filter {
    name   = random_pet.name.id
    values = ["ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "webserver" {
  ami           = data.aws_ami.ubuntu-linux-1404.id
  instance_type = "t1.micro"
  user_data     = file("init-script.sh")
  tags = {
    Name = "instance-${random_pet.name.id}"
  }
}

