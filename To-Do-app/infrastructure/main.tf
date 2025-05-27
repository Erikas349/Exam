provider "aws" {
  region = "eu-central-1"
}

resource "aws_instance" "app_server" {
  ami           = "ami-02b7d5b1e55a7b5f1"
  instance_type = "t2.micro"

  key_name = "todo-app-key"

  vpc_security_group_ids = [aws_security_group.allow_ssh.id]

  tags = {
    Name = "TodoApp"
  }

  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y docker
              sudo service docker start
              docker run -d -p 80:80 your-dockerhub/image-name
              EOF
}

resource "aws_security_group" "todo-app-security" {
  name        = "todo-app-security"
  description = "Allow SSH and HTTP"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
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
