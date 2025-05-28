# NCAA Game Highlights – Project #5

Welcome to my **Project #5: NCAA Game Highlights**! This containerized pipeline fetches NCAA game highlights using RapidAPI, processes the media with AWS MediaConvert, and leverages Terraform to provision the required AWS infrastructure. This project is designed to give you hands-on experience with Docker, AWS services, and Infrastructure as Code (IaC) using Terraform all in one streamlined solution.

---

## Project Overview

This project demonstrates how to:
- **Fetch Highlights:** Query the Sports Highlights API (via RapidAPI) for NCAA game highlights.
- **Process Videos:** Retrieve video URLs from the API, download them, and store them in an S3 bucket.
- **Media Conversion:** Use AWS MediaConvert to transcode videos (adjusting codec, resolution, and bitrate).
- **Containerization & IaC:** Run the entire pipeline inside a Docker container while provisioning resources using Terraform.

---

### Key Features

- **RapidAPI Integration:** Access NCAA game highlights using a free-tier RapidAPI endpoint.
- **AWS-Powered Workflow:** Seamlessly integrates AWS S3 for storage and AWS MediaConvert for video processing.
- **Dockerized Pipeline:** Containerize your entire workflow for consistent deployments.
- **Terraform Automation:** Provision all AWS resources (VPC, S3, IAM, ECR, ECS, etc.) with repeatable Terraform scripts.
- **Secure Configuration:** Manage sensitive keys and configuration via environment variables and AWS Secrets Manager.

---

### Technical Diagram

![Snap](https://github.com/user-attachments/assets/f3c4f55e-cea1-4147-96cc-2473e9e09636)

### File Structure

```bash
src/
├── Dockerfile                # Instructions to build the Docker image
├── config.py                 # Loads environment variables with sensible defaults
├── fetch.py                  # Fetches NCAA highlights from RapidAPI and stores metadata in S3
├── mediaconvert_process.py   # Submits a job to AWS MediaConvert to process a video
├── process_one_video.py      # Downloads the first video from S3 JSON metadata and re-uploads it
├── run_all.py                # Orchestrates the execution of all scripts
├── requirements.txt          # Python dependencies for the project
├── .env                      # Environment variables (API keys, AWS credentials, etc.)
└── .gitignore                # Files to exclude from Git
terraform/
├── main.tf                   # Main Terraform configuration file
├── variables.tf              # Variables
├── secrets.tf                # AWS Secrets Manager and sensitive data provisioning
├── iam.tf                    # IAM roles and policies
├── ecr.tf                    # ECR repository configuration
├── ecs.tf                    # ECS cluster and service configuration
├── s3.tf                   # S3 bucket provisioning for video storage
├── container_definitions.tpl # Template for container definitions
├── terraform.tfvars          # Variables used in the Terraform configuration
└── outputs.tf                # Outputs from Terraform
```

## Prerequisites

Before you dive in, make sure you have:
- RapidAPI Account: Sign up at RapidAPI and subscribe to the Sports Highlights API (using NCAA highlights for free).
- Docker: Verify installation with docker --version
- AWS CLI: Ensure AWS CLI is installed and configured (aws --version)
- Python 3: Check your Python version with python3 --version
- AWS Account Details: Your AWS Account ID and valid IAM access keys.

Environment Configuration
### 1. Create the .env File for Local Runs
In the root of your project (or within the src directory), create a file named .env and paste the following content. Update the placeholder values with your actual credentials and configuration details. This file will be used when running the project locally.

``` env
# .env

API_URL=https://sport-highlights-api.p.rapidapi.com/basketball/highlights
RAPIDAPI_HOST=sport-highlights-api.p.rapidapi.com
RAPIDAPI_KEY=your_rapidapi_key_here
AWS_ACCESS_KEY_ID=your_aws_access_key_id_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key_here
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET_NAME=your_S3_bucket_name_here
AWS_REGION=us-east-1
DATE=2023-12-01
LEAGUE_NAME=NCAA
LIMIT=5
MEDIACONVERT_ENDPOINT=https://your_mediaconvert_endpoint_here.amazonaws.com
MEDIACONVERT_ROLE_ARN=arn:aws:iam::your_account_id:role/YourMediaConvertRole
INPUT_KEY=highlights/basketball_highlights.json
OUTPUT_KEY=videos/first_video.mp4
RETRY_COUNT=3
RETRY_DELAY=30
WAIT_TIME_BETWEEN_SCRIPTS=60
```

### 2. Create the terraform.tfvars File for Deploying Terraform Code

Within the terraform directory, create a file named terraform.tfvars and paste the following content. You can update the values as needed. This file will be used to deploy your Terraform code and provision the AWS resources for the project. You have the option to enter your own project name by updating the project_name variable. Additionally, if you wish to use a custom MediaConvert role, provide its ARN in the mediaconvert_role_arn variable. For example, you might expect a value like: arn:aws:iam::123456789012:role/YourCustomMediaConvertRole. If left blank, the default role that is created during provisioning will be used.

``` tf
# terraform.tfvars

aws_region                = "us-east-1" # your preferred region here
project_name              = "your_project_name_here"  # Enter your own project name here
s3_bucket_name            = "your_S3_bucket_name_here"
ecr_repository_name       = "your_ecr_repository_name_here"

rapidapi_ssm_parameter_arn = "arn:aws:ssm:us-east-1:xxxxxxxxxxxx:parameter/myproject/rapidapi_key"

mediaconvert_endpoint     = "https://your_mediaconvert_endpoint_here.amazonaws.com"
mediaconvert_role_arn     = "" 
# Optionally, specify your custom MediaConvert role ARN here. For example:
# mediaconvert_role_arn = "arn:aws:iam::123456789012:role/YourCustomMediaConvertRole"
# Leaving this string empty will use the role that is automatically created by the Terraform scripts.

retry_count               = 5
retry_delay               = 60
```
Make sure to replace placeholder values with your actual configuration details.


### Setup & Deployment

### 1. Clone the Repository
```bash
git clone https://github.com/kingdave4/NCAA_GamehighLight.git
cd NCAA_GamehighLight/src
```

### 2. Add Your API Key to AWS Secrets Manager
Store your RapidAPI key securely:
```bash
aws secretsmanager create-secret \
    --name my-api-key \
    --description "API key for accessing the Sports Highlights API" \
    --secret-string '{"api_key":"YOUR_ACTUAL_API_KEY"}' \
    --region us-east-1
```

### 3. Update the .env File
Ensure that your .env file (created earlier) contains all necessary configuration values and is secured:
``` bash
chmod 600 .env
```

## Build & Run Locally with Docker
Build the Docker image:
``` bash
docker build -t highlight-processor .
```
Run the container:
``` bash
docker run -d --env-file .env highlight-processor
```

The container executes the pipeline: fetching highlights, processing a video, and submitting a MediaConvert job. Verify the output files in your S3 bucket:
- JSON metadata file
- Raw video in videos/
- Processed video in processed_videos/

## Terraform & Deployment to AWS
Provision AWS Resources with Terraform

### 1. Navigate to the Terraform directory:
``` bash
cd terraform
```

### 2. Initialize the Terraform workspace:
``` bash
terraform init
```

### 3. Validate the configuration:
``` bash
terraform validate
```

### 4. Preview the execution plan:
``` bash
terraform plan
```
### 5. Apply the configuration (using your variable file):
``` bash
terraform apply -var-file="terraform.tfvars"
```

## Deploy Docker Image to AWS ECR
### 1. Log in to AWS ECR:

``` bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
```
### 2. Build, tag, and push the Docker image:

``` bash
docker build -t highlight-pipeline:latest .
docker tag highlight-pipeline:latest <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/highlight-pipeline:latest
docker push <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/highlight-pipeline:latest
```

### Clean up and destroy all the AWS resources that was created.
``` bash
terraform destroy -auto-approve
```

## Challenges I Overcame

This Challlenge was annoying but it felt very satifying after completing it and finding the issue.

1️⃣ ECS Task Restart Loop: The ECS service was repeatedly starting and stopping tasks, leading to a continuous loop. This issue was traced back to application or configuration errors causing the tasks to stop unexpectedly.

2️⃣ IAM PassRole Permission for MediaConvert: The ECS tasks were unable to create processed highlight videos due to insufficient permissions, specifically lacking the iam:PassRole permission required for AWS Elemental MediaConvert. I addressed this by setting up the necessary IAM roles and policies, granting the ECS tasks the appropriate permissions to interact with MediaConvert. 


### Troubleshooting

ECS Task Failures:

- Check the stopped reason and exit code for tasks in the ECS console to identify underlying issues.
- Did some research and with the help of chatgpt i found the reason to why it kept failing.

MediaConvert Permission Errors:
- Verify that the IAM roles associated with ECS tasks include the necessary permissions, such as iam:PassRole, to allow interaction with MediaConvert.
- Review the IAM policies to ensure they grant access to the required AWS resources and services.

By systematically addressing these challenges and refining the IAM configurations, the project now operates smoothly, with ECS tasks running as expected and MediaConvert processing videos without permission issues.

### Key takeaways from Project #5:
- Leveraging containerization (Docker) to ensure consistency.
- Integrating multiple AWS services (S3, MediaConvert, ECS) for a robust media pipeline.
- Automating infrastructure setup using Terraform.
- Emphasizing secure configuration management via environment variables and Secrets Manager.

### Future Enhancements
- Expand Terraform scripts to provision additional AWS resources.
- Increase the number of videos processed concurrently.
- Transition from static date queries to dynamic time ranges (e.g., last 30 days).
- Improve logging and error handling for enhanced observability.
