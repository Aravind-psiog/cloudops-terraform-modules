#!/bin/bash
# Update the package index
apt update -y

# Install Apache web server
apt install -y apache2

# Start the Apache service
systemctl start apache2

# Enable Apache to start on boot
systemctl enable apache2

# Optional: Create a custom index.html file
echo "<html><h1>Server set-up by terraform</h1><img src='https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjJ2cmdjandsbHNoOHlidHRjdjZvamV3Mm4yY3RyNjM1MWNvYXBuMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/n5LZKpnnyXI2D99XN2/giphy.webp' alt='Computer man' style='width:100px;height:100px;'></html>" > /var/www/html/index.html
