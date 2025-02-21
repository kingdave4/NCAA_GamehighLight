# terraform.tfvars

aws_region                = "us-east-1"
project_name             = "highlight-pipeline-final"
s3_bucket_name           = "ncaaahighlightsfinal-king2"
ecr_repository_name      = "highlight-pipeline2-final"

rapidapi_ssm_parameter_arn = "arn:aws:ssm:us-east-1:636772248290:parameter/myproject/rapidapi_key"

mediaconvert_endpoint     = "https://q25wbt2lc.mediaconvert.us-east-1.amazonaws.com"
mediaconvert_role_arn     = "arn:aws:iam::636772248290:role/highlight-pipeline-final-mediaconvert-role" # Leaving the string empty will use the role that is created

retry_count                = 3
retry_delay                = 60
