output bucketName {
  value       = aws_s3_bucket.example.id
  sensitive   = false
  description = "description"
  depends_on  = []
}


output bucketArn {
  value       = aws_s3_bucket.example.arn
  sensitive   = false
  description = "description"
  depends_on  = []
}