variable "region" {
  default = "eu-central-1"
}

variable "ami" {
  default = "ami-02b7d5b1e55a7b5f1"
}

variable "instance_type" {
  default = "t2.micro"
}

variable "key_name" {
  default = "todo-app-key"
}

variable "vpc_id" {
  description = "The ID of the VPC where the EC2 instance will be launched"
  default     = "vpc-00773d4d01009da90"
  
}
variable "subnet_id" {
  description = "The ID of the subnet where the EC2 instance will be launched"
  default     = "subnet-0db6a9503152ca23a"
}
variable "security_group_name" {
  description = "The name of the security group to be used for the EC2 instance"
  default     = "todo-app-security"
}
