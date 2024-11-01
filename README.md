# SparkEMR Commander

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) 
![Amazon EMR](https://img.shields.io/badge/Amazon%20EMR-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)

A powerful command-line tool and API for managing and deploying Spark jobs on Amazon EMR clusters. EMRRunner simplifies the process of submitting and managing Spark jobs while handling all the necessary environment setup.

## 🚀 Features

- Command-line interface for quick job submission
- RESTful API for programmatic access
- Support for both client and cluster deploy modes
- Automatic S3 synchronization of job files
- Configurable job parameters
- Easy dependency management
- Bootstrap action support for cluster setup

## 📋 Prerequisites

- Python 3.9+
- AWS Account with EMR access
- Configured AWS credentials
- Active EMR cluster

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/SparkEMRCommander.git
cd SparkEMRCommander

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install the package
pip install -e .
```

## ⚙️ Configuration

### AWS Configuration
Create a `.env` file in the project root with your AWS configuration:

```env
AWS_ACCESS_KEY=your_access_key
AWS_SECRET_KEY=your_secret_key
AWS_REGION=your_region
EMR_CLUSTER_ID=your_cluster_id
S3_PATH=s3://your-bucket/path
```

### Bootstrap Actions
For EMR cluster setup with required dependencies, create a bootstrap script (`bootstrap.sh`):

```bash
#!/bin/bash -xe

# Example structure of a bootstrap script
# Create and activate virtual environment
python3 -m venv /home/hadoop/myenv
source /home/hadoop/myenv/bin/activate

# Install system dependencies
sudo yum install python3-pip -y
sudo yum install -y [your-system-packages]

# Install Python packages
pip3 install [your-required-packages]

deactivate
```

Upload the bootstrap script to S3 and reference it in your EMR cluster configuration.

## 💻 Usage

### Command Line Interface

Start a job in client mode:
```bash
emrrunner start --job job_name --step step_name
```

Start a job in cluster mode:
```bash
emrrunner start --job job_name --step step_name --deploy-mode cluster
```

### API Endpoints

Start a job via API:
```bash
curl -X POST http://localhost:8000/api/v1/emr/job/start \
     -H "Content-Type: application/json" \
     -H "X-API-Key: your_api_key" \
     -d '{"job_name": "example_job", "step": "example_step"}'
```

## 📁 Project Structure

```
SparkEMRCommander/
├── app/
│   ├── __init__.py
│   ├── cli.py              # Command-line interface
│   ├── emr_client.py       # EMR interaction logic
│   ├── emr_job_api.py      # Flask API
│   └── config.py           # Configuration management
├── bootstrap/
│   └── bootstrap.sh        # EMR bootstrap script
├── requirements.txt
└── setup.py
```

## 🔧 Development

To contribute to SparkEMR Commander:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 💡 Best Practices

1. **Bootstrap Actions**
   - Keep bootstrap scripts modular
   - Version control your dependencies
   - Use specific package versions
   - Test bootstrap scripts locally when possible
   - Store bootstrap scripts in S3 with versioning enabled

2. **Job Dependencies**
   - Maintain a requirements.txt for each job
   - Use virtual environments
   - Document system-level dependencies
   - Test dependencies in a clean environment

## 🔒 Security

- Uses API key authentication for endpoints
- Supports AWS credential management
- Validates all input parameters
- Secure handling of bootstrap scripts

## 📝 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🐛 Bug Reports

If you discover any bugs, please create an issue on GitHub with:
- Your operating system name and version
- Any details about your local setup that might be helpful in troubleshooting
- Detailed steps to reproduce the bug

## ✨ Acknowledgements

- AWS EMR Team
- Flask Framework
- Python Community

---

Built with ❤️ using Python and AWS EMR