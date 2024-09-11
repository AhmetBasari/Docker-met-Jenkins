provider "aws" {
  region = "us-west-2"  # Adjust the region as needed
}

resource "aws_instance" "bookstore" {
  ami           = "ami-0182f373e66f89c85"  # Use Amazon Linux 2 AMI or suitable AMI for your region
  instance_type = "t2.micro"
  
  tags = {
    Name = "Bookstore-Web-Server"
  }

  user_data = file("user-data.sh")  # Use a shell script to install Docker, Jenkins, or other dependencies
}

output "instance_ip" {
  value = aws_instance.bookstore.public_ip
}
