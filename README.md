# EMR Job Runner

## Overview

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Amazon EMR](https://img.shields.io/badge/Amazon%20EMR-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)

The EMR Job Runner is a Flask-based application that interfaces with AWS EMR (Elastic MapReduce) to manage and execute Spark jobs. This application allows users to start EMR jobs by providing job names and steps, and it handles API key validation for security.

## Features

- Start EMR jobs with specified configurations.
- Validate input using Marshmallow schemas.
- Handle errors gracefully and provide meaningful error messages.
- Built-in decorators for API key validation.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Continuous Integration](#continuous-integration)
- [Bootstrap Action](#bootstrap-action)
- [Deployment](#deployment)


## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Haabiy/EMRRunner.git
   cd EMRRunner
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate 
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory of the project and set your AWS and API key values:

   ```bash
   AWS_ACCESS_KEY_ID=<your_access_key>
   AWS_SECRET_ACCESS_KEY=<your_secret_key>
   AWS_REGION=<your_region>
   EMR_CLUSTER_ID=<your_cluster_id>
   BUCKET_NAME=<your_bucket_name>
   S3_PATH=<your_s3_path>
   API_KEY_VALUE=<your_api_key>
   ```

   <span style='color:#7493c4'> ⦿ Note: It is recommended to export these keys in the terminal explicitly before running the application to ensure they are available in your environment.</span>

## Configuration

The application reads configuration values from environment variables stored in a `.env` file. Ensure you fill in the required keys as specified above.

## Usage

Run the Flask application using the following command:

```bash
python app.py
```

The application will start on `http://0.0.0.0:8000`.

## API Endpoints

### Start EMR Job

- **Endpoint:** `/api/v1/emr/job/start`
- **Method:** `POST`
- **Headers:**
  - `X-Api-Key`: Your API key
- **Payload:**

  ```json
  {
      "job_name": "string",
      "step": "string"
  }
  ```

- **Responses:**
  - `200 OK`: Job started successfully.
  - `400 Bad Request`: Invalid input.
  - `401 Unauthorized`: Invalid API key.
  - `500 Internal Server Error`: AWS EMR error or unexpected error.

## Testing

To run the tests using `pytest`, execute the following command:

```bash
pytest
```

To exclude `__init__.py` files from being tested, you can specify the following options:

```bash
pytest --ignore=app/__init__.py
```

or

```bash
pytest --ignore-glob="**/__init__.py"
```

### Dependencies for Testing

For testing purposes, you will need the following files:

#### dependencies.py

```python
def main():
    try:
        print('Hello World')
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()
```

#### job.py

```python
from pyspark.sql import SparkSession
import logging

logging.basicConfig(level=logging.INFO)

def main():
    try:
        # Initialize Spark session
        spark = SparkSession.builder.appName("SamplePySparkJob").getOrCreate()

        # S3 input and output paths
        input_path = "s3://please-indicate-your-path/input_data.csv"
        output_path = "s3://please-indicate-your-path/SampleTest.csv"

        # Read input data
        df = spark.read.csv(input_path, header=True, inferSchema=True)

        # Perform a simple transformation (in this case, just selecting a subset of columns)
        transformed_df = df.select("Name", "Age")

        # Write the result back to S3 in Parquet format
        transformed_df.write.mode("overwrite").csv(output_path)

        # Stop the Spark session
        spark.stop()
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()
```

## Continuous Integration

To set up continuous integration, you can configure your CI tool (like GitHub Actions) to run `pytest` on every push or pull request. 

### Setting Environment Variables

To ensure the application works correctly in CI/CD pipelines, you need to set environment variables. This can be done by following these steps:

1. Go to **Settings** in your repository.
2. Navigate to **Secrets and Variables**.
3. Click on **Actions**.
4. Under **Repository Secrets**, add the following environment variables:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION`
   - `EMR_CLUSTER_ID`
   - `BUCKET_NAME`
   - `S3_PATH`
   - `API_KEY_VALUE`

These secrets will be securely accessed by the CI pipeline during execution. Here’s an example of a GitHub Actions workflow:

```yaml
name: CI

on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    env:
      AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
      AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      AWS_REGION: ${{ secrets.AWS_REGION }}
      EMR_CLUSTER_ID: ${{ secrets.EMR_CLUSTER_ID }}
      BUCKET_NAME: ${{ secrets.BUCKET_NAME }}
      S3_PATH: ${{ secrets.S3_PATH }}
      API_KEY_VALUE: ${{ secrets.API_KEY_VALUE }}
    steps:
      - name: Check out the code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m venv venv
          . venv/bin/activate
          pip install -r requirements.txt

      - name: Run tests
        run: |
          . venv/bin/activate
          pytest --ignore=app/__init__.py
```

## Bootstrap Action

A bootstrap action is used to set up the environment on the EMR cluster before any tasks are run. In this case, it creates and activates a virtual environment to avoid compatibility issues with Amazon's prebuilt libraries. The bootstrap action script (`bootstrap.sh`) is as follows:

```bash
#!/bin/bash -xe

# Create and activate a virtual environment
python3 -m venv /home/hadoop/venv
source /home/hadoop/venv/bin/activate

# Install pip for Python 3.x
sudo yum install python3-pip -y
sudo yum install -y python-psycopg2

# Install required packages
pip3 install \
    boto3==1.26.53 \
    pyspark==3.5.0 \
    numpy==1.26.3 \
    openpyxl==3.1.2 \
    pandas==1.5.3 \
    polars==0.20.5 \
    psycopg2-binary==2.9.9 \
    python-dotenv==1.0.0 \
    s3fs==2023.4.0 \
    SQLAlchemy==1.4.47 \
    python-dateutil==2.8.2 \
    connectorx==0.3.2 \
    pyarrow==11.0.0 \
    Unidecode==0.4.1 \
    rapidfuzz==3.1.1

deactivate
```

### Explanation
- The script sets up a Python virtual environment in `/home/hadoop/venv`.
- It installs necessary packages - (Include all libraries found in your `requirements.txt` file)

## Deployment

When running Spark jobs on EMR through this application, you can deploy the job in **two modes**:

1. **Client Mode** (default):
   - In this mode, the Spark driver runs on the master node and submits tasks to worker nodes.
   - The `spark-submit` command is executed as follows:
   
   ```bash
   spark-submit --conf spark.pyspark.python=/home/hadoop/venv/bin/python --py-files dependencies.py job.py
   ```

   - This is useful for small to medium jobs, where you want the driver logs to remain on the master node.

2. **Cluster Mode**:
   - In this mode, both the driver and tasks are distributed across the EMR cluster.
   - The `spark-submit` command is executed in **cluster mode** as follows:

   ```bash
   spark-submit --deploy-mode cluster --conf spark.pyspark.python=/usr/bin/python3 --py-files dependencies.py job.py
   ```

   - This mode is ideal for larger jobs, as it allows for better distribution of resources and fault tolerance by leveraging the full EMR cluster.

### How to Choose the Deployment Mode

The mode you choose depends on the scale of the job and where you prefer the driver to run. In the `create_step_config` function in the code, you can switch between these modes based on the requirements.