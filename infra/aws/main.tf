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

# data "aws_ami" "ubuntu" {
#   most_recent = true

#   filter {
#     name   = "name"
#     values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
#   }

#   filter {
#     name   = "virtualization-type"
#     values = ["hvm"]
#   }

#   owners = ["099720109477"]
# }

# resource "aws_instance" "webserver" {
#   ami           = data.aws_ami.ubuntu.id
#   instance_type = "t1.micro"
#   user_data     = file("init-script.sh")

#   tags = {
#     Name = random_pet.name.id
#   }
# }

# Permission for Cognito to invoke the Lambda function
resource "aws_lambda_permission" "allow_cognito_invoke" {
  statement_id  = "AllowCognitoInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.post_verification_lambda.function_name
  principal     = "cognito-idp.amazonaws.com"

  # Specify the User Pool ARN to restrict the source
  source_arn = aws_cognito_user_pool.user_pool.arn
}

resource "aws_cognito_user_pool" "user_pool" {
  name = "user-pool"

  alias_attributes = ["email", "preferred_username"]

  # Configure verification email
  verification_message_template {
    email_subject        = "Verify your email for our app"
    email_message        = "Hello, please verify your email by entering the code: {####}"
    default_email_option = "CONFIRM_WITH_CODE"
  }

  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_uppercase = true
    require_numbers   = true
    require_symbols   = false
  }

  auto_verified_attributes = ["email"]

  lambda_config {
    post_confirmation = aws_lambda_function.post_verification_lambda.arn
  }
}

resource "aws_cognito_user_pool_domain" "user_pool_domain" {
  domain       = "example-user-pool"
  user_pool_id = aws_cognito_user_pool.user_pool.id
}

resource "aws_cognito_user_pool_client" "user_pool_client" {
  name            = "user-pool-client"
  user_pool_id    = aws_cognito_user_pool.user_pool.id
  generate_secret = false
}

resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role_test"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })

  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",  # For basic execution (CloudWatch logging)
    "arn:aws:iam::aws:policy/AmazonCognitoPowerUser"  # For Cognito operations
  ]
}

resource "aws_lambda_function" "post_verification_lambda" {
  function_name = "post_verification_function"
  role          = aws_iam_role.lambda_execution_role.arn
  handler       = "hello.lambda_handler"
  runtime       = "python3.9"

  filename = "functions/hello.zip"
  source_code_hash = filemd5("functions/hello.zip")
}

output "user_pool_id" {
  value = aws_cognito_user_pool.user_pool.id
}

output "user_pool_client_id" {
  value = aws_cognito_user_pool_client.user_pool_client.id
}

output "user_pool_domain" {
  value = aws_cognito_user_pool_domain.user_pool_domain.domain
}
