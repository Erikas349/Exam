provider "aws" {
  region = var.region
}

data "aws_security_group" "todo_app_security" {
  filter {
    name   = "group-name"
    values = ["todo-app-security"]
  }

  filter {
    name   = "vpc-id"
    values = ["vpc-00773d4d01009da90"]
  }
}

resource "aws_instance" "TodoApp" {
  ami                         = var.ami
  instance_type               = var.instance_type
  key_name                    = var.key_name
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [data.aws_security_group.todo_app_security.id]
  associate_public_ip_address = true

  tags = {
    Name = "TodoApp"
  }

  lifecycle {
   prevent_destroy = true
  }
}