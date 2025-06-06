output "instance_ip" {
    description = "Public IP of the EC2 instance"
  value = aws_instance.TodoApp.public_ip
}
output "instance_id" {
  description = "The ID of the EC2 instance"
  value       = aws_instance.TodoApp.id
}
