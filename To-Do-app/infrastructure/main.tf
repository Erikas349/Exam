provider "aws" {
  region     = "eu-central-1"
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

resource "aws_instance" "todo_app" {
  ami           = "ami-0fc5d935ebf8bc3bc" # Amazon Linux 2023 AMI
  instance_type = "t2.micro"
  key_name      = var.key_name

  vpc_security_group_ids = [aws_security_group.todo_app_sg.id]

  tags = {
    Name = "ToDoAppInstance"
  }
}

resource "aws_security_group" "todo_app_sg" {
  name        = "todo-app-sg"
  description = "Allow SSH and app traffic"
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 5000
    to_port     = 5000
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
