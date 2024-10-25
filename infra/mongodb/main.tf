terraform {
  required_providers {
    mongodbatlas = {
      source  = "mongodb/mongodbatlas"
      version = "~> 1.7" # MongoDB Atlas provider version
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0" # AWS provider version
    }
  }
}

provider "aws" {
  region = "us-east-1"

}

provider "mongodbatlas" {
  public_key  = var.public_key
  private_key = var.private_key
}

# Create a MongoDB Atlas Cluster
resource "mongodbatlas_cluster" "example" {
  project_id                  = var.project_id
  name                        = var.mongo_cluster
  provider_name               = "AWS"
  provider_region_name        = "US_EAST_1"
  provider_instance_size_name = "M10"
}

# Create a MongoDB Database User
resource "mongodbatlas_database_user" "db_user" {
  project_id         = var.project_id     # Same as the project ID of your cluster
  username           = var.mongo_username # Define your database username
  password           = var.mongo_password # Define your database password (consider storing this securely)
  auth_database_name = "admin"            # The authentication database, usually "admin"
  roles {
    role_name     = "readWrite"
    database_name = "admin" # Apply the role to the "admin" database (or your target DB)
  }
  roles {
    role_name     = "atlasAdmin" # Adding Atlas Admin role
    database_name = "admin"
  }

  depends_on = [mongodbatlas_cluster.example]
}

resource "random_uuid" "secret_id" {}

# Create an AWS Secrets Manager secret to store MongoDB credentials
resource "aws_secretsmanager_secret" "mongo_secret" {
  name        = "mongo-db-secret-${random_uuid.secret_id.result}"
  description = "MongoDB credentials and connection information"
}

resource "aws_secretsmanager_secret_version" "mongo_secret_version" {
  secret_id = aws_secretsmanager_secret.mongo_secret.id
  secret_string = jsonencode({
    username = var.mongo_username
    password = var.mongo_password
    uri      = <<EOT
${replace(mongodbatlas_cluster.example.connection_strings[0].standard_srv, "mongodb+srv://", "")}
EOT
    db_name  = "admin"
  })
}


# Generate a random UUID for the S3 bucket name
resource "random_uuid" "bucket_id" {}

# Create an S3 Bucket
resource "aws_s3_bucket" "my_bucket" {
  bucket = "mongo-backup-${random_uuid.bucket_id.result}"

  tags = {
    Name = "MyDataBucket"
  }
}
resource "aws_s3_bucket_public_access_block" "my_bucket_public_access" {
  bucket = aws_s3_bucket.my_bucket.id

  block_public_acls       = false
  ignore_public_acls      = false
  block_public_policy     = false
  restrict_public_buckets = false
}

# Set up a bucket policy for public read access (as an example, adjust as needed)
resource "aws_s3_bucket_policy" "bucket_policy" {
  bucket = aws_s3_bucket.my_bucket.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action    = ["s3:GetObject"],
        Effect    = "Allow",
        Resource  = "${aws_s3_bucket.my_bucket.arn}/*",
        Principal = "*"
      }
    ]
  })
}

# Upload JSON files to S3
resource "aws_s3_object" "json_files" {
  for_each = fileset("${path.module}/data", "*.json")
  bucket   = aws_s3_bucket.my_bucket.id
  key      = each.value
  source   = "${path.module}/data/${each.value}"
}

resource "null_resource" "run_mongo_script" {
  provisioner "local-exec" {
    command = "python etl_mongo.py"

  }
  triggers = {
    # Generate a file hash to detect changes
    etl_file_hash = "${filesha256("etl_mongo.py")}"
  }

  depends_on = [mongodbatlas_cluster.example]
}
