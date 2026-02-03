variable "region" {
  description = "AWS Region to deploy to"
  type        = string
  default     = "ap-southeast-2"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "vssc-qdpc"
}

variable "db_password" {
  description = "Password for the RDS database instance"
  type        = string
  default     = "samplepassword123"
}

# variable "instance_type" {
#   description = "EC2 Instance Type"
#   type        = string
#   default     = "t3.small"
# }

# variable "key_name" {
#   description = "Name of the existing EC2 Key Pair to allow SSH access"
#   type        = string
#   # User must provide this, or created separately
#   default = "my-key-pair"
# }

# variable "ecr_registry_url" {
#   description = "URL of the ECR registry (without repo name)"
#   type        = string
#   default     = "637423214672.dkr.ecr.ap-southeast-2.amazonaws.com"
# }
