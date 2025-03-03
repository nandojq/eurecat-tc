terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>3.3.0"
    }
  }
}

provider "aws" {
  region = "eu-west-3"
}

resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"
  assume_role_policy = jsonencode({
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_budgets_budget" "testbudget" {
  name              = "monthly-budget"
  budget_type       = "COST"
  limit_amount      = "20.0"
  limit_unit        = "USD"
  time_unit         = "MONTHLY"
  time_period_start = "2025-03-01_00:01"
}

# resource "aws_lambda_function" "lambda_function_1" {
#   function_name    = "ingestion"
#   role             = aws_iam_role.lambda_exec.arn
#   handler          = "lambda1.handler"
#   runtime          = "python3.8"
#   timeout          = 600
#   filename         = "C:\\Users\\Fer\\Desktop\\Code\\eurecat-tc\\src\\ingestion\\ingestion.zip"
#   source_code_hash = filebase64sha256("C:\\Users\\Fer\\Desktop\\Code\\eurecat-tc\\src\\ingestion\\ingestion.zip")
# }


resource "aws_db_instance" "rds_instance" {
  identifier          = "nba-database"
  engine              = "mysql"
  instance_class      = "db.t3.micro"
  allocated_storage   = 20
  username            = "admin"
  password            = "mysuperlongpassword"
  publicly_accessible = true
}
