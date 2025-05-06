provider "aws" {
  region = "eu-central-1"
}

resource "aws_instance" "todo_app" {
    ami           = "ami-0c55b159cbfafe1f0" # Amazon Linux 2 AMI
    instance_type = "t2.micro"
    key_name      = "todo-app-key"
    security_groups = ["todo-app-security"]

    user_data = <<-EOF
                #!/bin/bash
                docker-compose -f /home/ec2-user/docker-compose.yml up -d
                EOF

    tags = {
        Name = "TodoApp"
    }
}

resource "aws_db_instance" "todo_db" {
    identifier = "todo-db"
    engine    = "postgress"
    instance_class = "db.t2.micro"
    allocated_storage = 20
    username = "admin"
    password = "var.db_password"
    skip_final_snapshot = true
}

resource "aws_security_group" "allow_app" {
  ingress = {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}