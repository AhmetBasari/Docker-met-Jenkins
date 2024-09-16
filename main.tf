provider "aws" {
  region = "us-west-2"  # Adjust the region as needed
}

resource "aws_security_group" "allow_http_prometheus" {
  name        = "allow_http_prometheus"
  description = "Allow HTTP and Prometheus traffic"
  vpc_id      = aws_vpc.main.id  # Ensure correct VPC

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "bookstore" {
  ami           = "ami-0182f373e66f89c85"  # Amazon Linux 2 AMI
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.allow_http_prometheus.id]

  tags = {
    Name = "Bookstore-Web-Server"
  }

  user_data = file("user-data.sh")  # Install Flask, Prometheus, or other dependencies via this script
}

output "instance_ip" {
  value = aws_instance.bookstore.public_ip
}
