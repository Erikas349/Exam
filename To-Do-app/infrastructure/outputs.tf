output "rds_endpoint" {
  value = aws_db_instance.todo_app_db.endpoint
}