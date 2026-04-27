# Terraform Naming Conventions

## Resource Naming Pattern
All resources should follow: {project}-{environment}-{resource_type}-{description}

Examples:
- S3 bucket: myapp-prod-s3-uploads
- Lambda function: myapp-dev-lambda-process-orders
- API Gateway: myapp-staging-apigw-main
- DynamoDB table: myapp-prod-dynamodb-users

## Variable Naming
- Use snake_case for all variable names
- Prefix with the resource type when possible
- Example: s3_bucket_name, lambda_function_arn, vpc_id

## Environment Values
- Use short codes: dev, staging, prod
- Always pass environment as a variable, never hardcode

## Tags
Every resource must have these tags:
- Name: Same as resource name
- Environment: dev / staging / prod
- Project: Project name
- ManagedBy: terraform

Example:
```hcl
tags = {
  Name        = "${var.project}-${var.environment}-s3-uploads"
  Environment = var.environment
  Project     = var.project
  ManagedBy   = "terraform"
}
```

## Module Naming
- Module folder names: lowercase, hyphens (e.g., s3-bucket, lambda-function)
- Module source reference: use relative paths for local modules
- Example: source = "./modules/s3-bucket"

## File Structure in Modules
Each module should have:
- main.tf — resource definitions
- variables.tf — input variables
- outputs.tf — output values
- README.md — module documentation
