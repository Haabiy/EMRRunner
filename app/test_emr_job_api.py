"""
test_app.py: Test suite for the EMR Job API

This module contains unit tests and integration tests for the EMR Job API.
It uses pytest for test execution and mocking.

Author: Your Name
Date: October 12, 2024
"""

import pytest
from unittest.mock import patch, MagicMock
from marshmallow import ValidationError
from app.emr_job_api import app, create_step_config, JobRequestSchema, API_SECRET
import os

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_step_config():
    """Unit test for create_step_config function."""
    job_name = "Test Job"
    step = "test_step"
    config = create_step_config(job_name, step)
    
    assert config['Name'] == job_name
    assert config['ActionOnFailure'] == 'CONTINUE'
    assert 'HadoopJarStep' in config
    assert 'Args' in config['HadoopJarStep']
    assert 'spark-submit' in config['HadoopJarStep']['Args'][-1]

def test_job_request_schema_valid():
    """Unit test for JobRequestSchema with valid data."""
    schema = JobRequestSchema()
    data = {"job_name": "Test Job", "step": "test_step"}
    result = schema.load(data)
    assert result == data

def test_job_request_schema_invalid():
    """Unit test for JobRequestSchema with invalid data."""
    schema = JobRequestSchema()
    data = {"job_name": "Test Job"}  # Missing 'step'
    with pytest.raises(ValidationError):
        schema.load(data)

@patch('app.emr_job_api.emr_client')
def test_start_emr_job_success(mock_emr_client, client):
    """Integration test for successful job start."""
    mock_emr_client.add_job_flow_steps.return_value = {'StepIds': ['s-123456']}
    
    response = client.post('/api/v1/emr/job/start', 
                           json={"job_name": "Test Job", "step": "test_step"},
                           headers={"X-Api-Key": os.getenv("API_KEY_VALUE")})
    
    assert response.status_code == 200
    assert response.json['success'] == True
    assert 'step_id' in response.json

def test_start_emr_job_unauthorized(client):
    """Integration test for unauthorized access."""
    response = client.post('/api/v1/emr/job/start', 
                           json={"job_name": "Test Job", "step": "test_step"},
                           headers={"X-Api-Key": "wrong_api_key"})
    
    assert response.status_code == 401

@patch('app.emr_job_api.emr_client')
def test_start_emr_job_invalid_input(mock_emr_client, client):
    """Integration test for invalid input."""
    response = client.post('/api/v1/emr/job/start', 
                           json={"job_name": "Test Job"},  # Missing 'step'
                           headers={"X-Api-Key": os.getenv("API_KEY_VALUE")})
    
    assert response.status_code == 400
    assert 'error' in response.json

@patch('app.emr_job_api.emr_client')
def test_start_emr_job_aws_error(mock_emr_client, client):
    """Integration test for AWS EMR error."""
    mock_emr_client.add_job_flow_steps.side_effect = Exception("AWS Error")
    
    response = client.post('/api/v1/emr/job/start', 
                           json={"job_name": "Test Job", "step": "test_step"},
                           headers={"X-Api-Key": os.getenv("API_KEY_VALUE")})
    
    assert response.status_code == 500
    assert 'error' in response.json

def test_404_error(client):
    """Test 404 Not Found error handler."""
    response = client.get('/non_existent_route')
    assert response.status_code == 404
    assert 'error' in response.json

def test_405_error(client):
    """Test 405 Method Not Allowed error handler."""
    response = client.get('/api/v1/emr/job/start')
    assert response.status_code == 405
    assert 'error' in response.json