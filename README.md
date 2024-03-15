# EMR Job Runner

This application facilitates the submission and monitoring of jobs on Amazon Elastic MapReduce (EMR) clusters through a Flask API.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
- [Deployment Mode](#deployment-mode)
- [Dependency Management](#dependency-management)
- [Troubleshooting](#troubleshooting)

## Overview

The EMR Job Runner provides a RESTful API to start and monitor jobs on EMR clusters. It enables users to submit job configurations and automatically adds them to the specified EMR cluster for execution. Additionally, users can check the status of individual job steps and monitor the overall cluster status through the provided endpoints.

## Prerequisites

Before using the EMR Job Runner, ensure you have the following:

- AWS IAM credentials with permissions to access EMR resources.
- An existing EMR cluster set up on your AWS account.
- Python installed on your local machine or server.
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) installed (`pip install boto3`).
- [Flask](https://flask.palletsprojects.com/en/2.1.x/installation/) installed (`pip install Flask`).
- [dotenv](https://pypi.org/project/python-dotenv/) installed (`pip install python-dotenv`).

## Setup

1. Clone this repository to your local machine or server.
2. Navigate to the project directory and install dependencies using `pip install -r requirements.txt`.
3. Set up your environment variables by creating a `.env` file in the project root directory. Include the following variables:

   ```
   AWS_ACCESS_KEY_ID=your_access_key_id
   AWS_SECRET_ACCESS_KEY=your_secret_access_key
   AWS_REGION=your_aws_region
   EMR_CLUSTER_ID=your_emr_cluster_id
   BUCKET_NAME=your_s3_bucket_name
   API_KEY_VALUE=your_api_key_value
   S3_PATH=your_s3_path
   ```

   Replace `your_access_key_id`, `your_secret_access_key`, `your_aws_region`, `your_emr_cluster_id`, `your_s3_bucket_name`, `your_api_key_value`, and `your_s3_path` with your actual AWS credentials and configurations.

4. Ensure your AWS IAM user has the necessary permissions to access EMR resources and perform the required actions.

## Usage

- Start an EMR job: Send a POST request to `/start_emr_job` with the job configuration in JSON format, including the `job_name` and `step`. Ensure to include the `apikey` header with the value of your API key.

- Check job status: Send a POST request to `/check_job_status` with the `step_id` of the job step you want to check. Include the `apikey` header with your API key.

- Check cluster status: Send a POST request to `/check_cluster_status`. Include the `apikey` header with your API key.

## Deployment Mode

When specifying the deployment mode as `cluster`, ensure to include the necessary dependencies such as `job.py` or `main.py` along with your job configuration. Additionally, include the following Spark configuration to avoid compatibility issues:

```
--conf spark.pyspark.python=/usr/bin/python3
```

## Dependency Management

To manage dependencies and ensure compatibility, it's recommended to use virtual environments. This isolates dependencies and prevents compatibility issues with Amazon's pre-built packages. Include the virtual environment activation command in your job configuration to streamline dependency management.

## Troubleshooting

- **Exporting Environment Variables**: When running the Flask application, ensure to explicitly export the `.env` file to set up the environment variables.

- **Checking Logs**: To troubleshoot issues, SSH into the primary node of your EMR cluster and view logs using the following command:

  ```
  ssh -i /path/to/your/KeyPair.pem hadoop@your_emr_master_public_dns
  yarn logs -applicationId your_application_id
  ```

Replace `/path/to/your/KeyPair.pem`, `your_emr_master_public_dns`, and `your_application_id` with your actual values.

--- 

Feel free to let me know if you have any question !