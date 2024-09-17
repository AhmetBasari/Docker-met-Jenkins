provider "aws" {
  region = "us-west-2"
}

resource "aws_instance" "bookstore" {
  ami           = "ami-0ebfd941bbafe70c6"
  instance_type = "t2.micro"

  tags = {
    Name = "Bookstore-Web-Server"
  }

  user_data = file("user-data.sh")  # Use a shell script to install Flask or other dependencies
}

output "instance_ip" {
  value = aws_instance.bookstore.public_ip
}
