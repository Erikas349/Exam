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