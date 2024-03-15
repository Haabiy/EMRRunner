#!/bin/bash -xe

# Create and activate a virtual environment
python3 -m venv myenv
source myenv/bin/activate
# Install pip for Python 3.x
sudo yum install python3-pip -y
sudo yum install -y python-psycopg2
# List installed packages (optional)
sudo python3 -m pip list

# Install required packages
pip3 install \
    boto3==1.26.53 \
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
    boto3==1.26.53 \
    numpy==1.26.3 \
    pandas==1.5.3 \
    polars==0.20.5 \
    rapidfuzz==3.1.1 \
    s3fs==2023.4.0 \
    SQLAlchemy==1.4.47 \
    tqdm==4.66.1

# List installed packages again (optional)
sudo python3 -m pip list
deactivate


