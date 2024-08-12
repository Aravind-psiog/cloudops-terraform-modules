#!/bin/bash
# Update the package index
yum update -y

# Install Apache web server
yum install -y httpd

# Start the Apache service
systemctl start httpd

# Enable Apache to start on boot
systemctl enable httpd

# Optional: Create a custom index.html file
echo "<html><h1>Welcome to your Apache server!</h1></html>" > /var/www/html/index.html
