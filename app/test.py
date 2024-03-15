from app import app
from flask import json
import unittest

class TestEMRJob(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_start_emr_job(self):
        input_data = {
            'job_name': 'test_job',
            'step': 'test_step'
        }
        headers = {'apikey': 'api_key_value'}

        # Sending a POST request to the /start_emr_job endpoint
        response = self.app.post('/start_emr_job', json=input_data, headers=headers)
        
        # Asserting the response status code
        self.assertEqual(response.status_code, 200)

    def test_start_emr_job_unauthorized(self):
        # Test case for unauthorized access
        input_data = {
            'job_name': 'test_job',
            'step': 'test_step'
        }
        headers = {'apikey': 'invalid_api_key'}
        response = self.app.post('/start_emr_job', json=input_data, headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_check_job_status_success(self):
        # Test case for checking job status successfully
        input_data = {
            'job_name': 'test_job',
            'step': 'test_step'
        }
        headers = {'apikey': 'api_key_value'}
        response = self.app.post('/check_job_status', json=input_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        # Add more assertions to check the response content or behavior

    def test_check_job_status_unauthorized(self):
        # Test case for unauthorized access to check job status
        input_data = {'step_id': 'test_step_id'}
        headers = {'apikey': 'invalid_api_key'}
        response = self.app.post('/check_job_status', json=input_data, headers=headers)
        self.assertEqual(response.status_code, 403)
        # Add more assertions to check the response content or behavior

    def test_check_cluster_status_success(self):
        # Test case for checking cluster status successfully
        headers = {'apikey': 'api_key_value'}
        response = self.app.post('/check_cluster_status', headers=headers)
        self.assertEqual(response.status_code, 200)
        # Add more assertions to check the response content or behavior

    def test_check_cluster_status_unauthorized(self):
        # Test case for unauthorized access to check cluster status
        headers = {'apikey': 'invalid_api_key'}
        response = self.app.post('/check_cluster_status', headers=headers)
        self.assertEqual(response.status_code, 403)
        # Add more assertions to check the response content or behavior

if __name__ == '__main__':
    unittest.main()
