# EMR Job Runner

## Overview

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

   **Note:** It is recommended to export these keys in the terminal explicitly before running the application to ensure they are available in your environment.

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

These secrets will be securely accessed by the CI pipeline during execution;
Here’s a basic example of a GitHub Actions workflow:

```yaml
name: CI

on: [push, pull_request]

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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```