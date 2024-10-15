# output "mongo_connection" {
#   value     = "mongodb+srv://${mongodbatlas_database_user.db_user.username}:${mongodbatlas_database_user.db_user.password}@${mongodbatlas_cluster.example.name}.wjdysd.mongodb.net/"
#   sensitive = true # Mark as sensitive to avoid exposing credentials
# }
output "mongo_connection" {
  value     = <<EOT
mongodb+srv://${mongodbatlas_database_user.db_user.username}:${mongodbatlas_database_user.db_user.password}@${replace(mongodbatlas_cluster.example.connection_strings[0].standard_srv, "mongodb+srv://", "")}
EOT
  sensitive = true
}




output "db_user_credentials" {
  value = {
    username = mongodbatlas_database_user.db_user.username
    password = mongodbatlas_database_user.db_user.password
  }
  sensitive = true
}
# Output the URLs of the uploaded JSON files
output "json_file_urls" {
  value = [for file in aws_s3_object.json_files : "https://${aws_s3_bucket.my_bucket.bucket}.s3.amazonaws.com/${file.key}"]
}
