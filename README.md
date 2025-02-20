# NCAA Game Highlights – Project #5

Welcome to **Project #5: NCAA Game Highlights**! This containerized pipeline fetches NCAA game highlights using RapidAPI, processes the media with AWS MediaConvert, and leverages Terraform to provision the required AWS infrastructure. This project is designed to give you hands-on experience with Docker, AWS services, and Infrastructure as Code (IaC) using Terraform—all in one streamlined solution.

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
├── variables.tf              # Variables used in the Terraform configuration
├── secrets.tf                # AWS Secrets Manager and sensitive data provisioning
├── iam.tf                    # IAM roles and policies
├── ecr.tf                    # ECR repository configuration
├── ecs.tf                    # ECS cluster and service configuration
├── s3.tf                   # S3 bucket provisioning for video storage
├── container_definitions.tpl # Template for container definitions
└── outputs.tf                # Outputs from Terraform

## Prerequisites

Before you dive in, make sure you have:
- RapidAPI Account: Sign up at RapidAPI and subscribe to the Sports Highlights API (using NCAA highlights for free).
- Docker: Verify installation with docker --version
- AWS CLI: Ensure AWS CLI is installed and configured (aws --version)
- Python 3: Check your Python version with python3 --version
- AWS Account Details: Your AWS Account ID and valid IAM access keys.


## Setup & Deployment

1. Clone the Repository
```bash
git clone https://github.com/kingdave4/NCAA_GamehighLight.git
cd NCAA_GamehighLight/src
```

2. Add Your API Key to AWS Secrets Manager

Store your RapidAPI key securely:

```bash
aws secretsmanager create-secret \
    --name my-api-key \
    --description "API key for accessing the Sports Highlights API" \
    --secret-string '{"api_key":"YOUR_ACTUAL_API_KEY"}' \
    --region us-east-1
```
3. Create the Required IAM Role/User

Open the AWS Management Console and navigate to IAM.

Create a role named HighlightProcessorRole with the following permissions:
- AmazonS3FullAccess
- MediaConvertFullAccess
- AmazonEC2ContainerRegistryFullAccess
Update the role’s trust policy (replace placeholders):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "ec2.amazonaws.com",
          "ecs-tasks.amazonaws.com",
          "mediaconvert.amazonaws.com"
        ],
        "AWS": "arn:aws:iam::<your-account-id>:user/<your-iam-user>"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

4. Update the .env File
Configure your .env with:
- RapidAPI_KEY
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- S3_BUCKET_NAME
- MEDIACONVERT_ENDPOINT (retrieve with aws mediaconvert describe-endpoints)
- MEDIACONVERT_ROLE_ARN (e.g., arn:aws:iam::your_account_id:role/HighlightProcessorRole)

Secure the file:
``` bash
chmod 600 .env
```

5. Build & Run Locally with Docker
Build the Docker image:
``` bash
docker build -t highlight-processor .
```
Run the container:
``` bash
docker run --env-file .env highlight-processor
```

The container executes the pipeline: fetching highlights, processing a video, and submitting a MediaConvert job. Verify the output files in your S3 bucket:
- JSON metadata file
- Raw video in videos/
- Processed video in processed_videos/

### Terraform & Deployment to AWS
Provision AWS Resources with Terraform
    1. Navigate to the Terraform directory:
``` bash
cd terraform
```
    2. Initialize the Terraform workspace:

``` bash
terraform init
```

    3. Validate the configuration:
``` bash
terraform validate
```

    4. Preview the execution plan:

``` bash
terraform plan
```
    5. Apply the configuration (using your variable file):

``` bash
terraform apply -var-file="terraform.tfvars"
```

### Deploy Docker Image to AWS ECR
    1. Log in to AWS ECR:

``` bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
```
    2. Build, tag, and push the Docker image:

``` bash
docker build -t highlight-pipeline:latest .
docker tag highlight-pipeline:latest <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/highlight-pipeline:latest
docker push <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/highlight-pipeline:latest
```

### Verification & What We Learned
After deployment, confirm that:

- The highlights JSON file is in your S3 bucket.
- The raw and processed videos are stored correctly.
- AWS MediaConvert jobs run successfully.

#### Key takeaways from Project #5:
- Leveraging containerization (Docker) to ensure consistency.
- Integrating multiple AWS services (S3, MediaConvert, ECS) for a robust media pipeline.
- Automating infrastructure setup using Terraform.
- Emphasizing secure configuration management via environment variables and Secrets Manager.

### Future Enhancements
- Expand Terraform scripts to provision additional AWS resources.
- Increase the number of videos processed concurrently.
- Transition from static date queries to dynamic time ranges (e.g., last 30 days).
- Improve logging and error handling for enhanced observability.

Happy coding, and enjoy exploring the powerful combination of containerization, AWS, and Terraform with Project #5: NCAA Game Highlights!

