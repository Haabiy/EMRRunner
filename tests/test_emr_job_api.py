import pytest
from flask import Flask, json
from unittest.mock import patch, MagicMock

# Import your API function
from app.emr_job_api import start_emr_job_endpoint

@pytest.fixture
def app():
    """Create and configure a test Flask application."""
    app = Flask(__name__)
    app.route('/api/emr/start-job', methods=['POST'])(start_emr_job_endpoint)
    return app

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

def test_start_emr_job_success(client):
    """Test successful EMR job start."""
    # Mock data
    test_data = {
        'job_name': 'test_job',
        'step': 'test_step',
        'deploy_mode': 'client'
    }
    
    # Mock the start_emr_job function
    with patch('app.emr_job_api.start_emr_job') as mock_start_job:
        mock_start_job.return_value = 'test-step-id'
        
        # Make request
        response = client.post(
            '/api/emr/start-job',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        # Assert response
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['step_id'] == 'test-step-id'
        assert data['details']['job_name'] == 'test_job'
        assert data['details']['step'] == 'test_step'
        assert data['details']['deploy_mode'] == 'client'
        
        # Verify function was called with correct parameters
        mock_start_job.assert_called_once_with(
            job_name='test_job',
            step='test_step'
        )

def test_missing_required_fields(client):
    """Test missing required fields in request."""
    # Test missing job_name
    test_data = {
        'step': 'test_step'
    }
    
    response = client.post(
        '/api/emr/start-job',
        data=json.dumps(test_data),
        content_type='application/json'
    )
    
    assert response.status_code == 500
    data = json.loads(response.data)
    assert 'error' in data
    assert 'details' in data

def test_empty_payload(client):
    """Test empty request payload."""
    response = client.post(
        '/api/emr/start-job',
        data=json.dumps({}),
        content_type='application/json'
    )
    
    assert response.status_code == 500
    data = json.loads(response.data)
    assert 'error' in data

def test_invalid_deploy_mode(client):
    """Test invalid deploy mode value."""
    test_data = {
        'job_name': 'test_job',
        'step': 'test_step',
        'deploy_mode': 'invalid_mode'
    }
    
    response = client.post(
        '/api/emr/start-job',
        data=json.dumps(test_data),
        content_type='application/json'
    )
    
    assert response.status_code == 200  # Since deploy_mode is optional

def test_emr_job_failure(client):
    """Test EMR job start failure."""
    test_data = {
        'job_name': 'test_job',
        'step': 'test_step'
    }
    
    with patch('app.emr_job_api.start_emr_job') as mock_start_job:
        mock_start_job.side_effect = Exception('EMR job failed')
        
        response = client.post(
            '/api/emr/start-job',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data['error'] == 'Unexpected error'
        assert 'EMR job failed' in data['details']

def test_invalid_json_payload(client):
    """Test invalid JSON payload."""
    response = client.post(
        '/api/emr/start-job',
        data='invalid json',
        content_type='application/json'
    )
    
    assert response.status_code == 500
    data = json.loads(response.data)
    assert 'error' in data