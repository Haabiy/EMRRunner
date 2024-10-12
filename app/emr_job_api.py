from flask import Flask, request, jsonify
import boto3
import os
from dotenv import load_dotenv
from functools import wraps
from marshmallow import Schema, fields, ValidationError

# Load environment variables
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# AWS and EMR configurations
AWS_CONFIG = {
    'ACCESS_KEY': os.getenv('AWS_ACCESS_KEY_ID'),
    'SECRET_KEY': os.getenv('AWS_SECRET_ACCESS_KEY'),
    'REGION': os.getenv('AWS_REGION')
}

EMR_CONFIG = {
    'CLUSTER_ID': os.getenv('EMR_CLUSTER_ID'),
    'S3_BUCKET': os.getenv('BUCKET_NAME'),
    'S3_PATH': os.getenv('S3_PATH')
}

API_KEY_VALUE = os.getenv('API_KEY_VALUE')

# Initialize Boto3 EMR client
emr_client = boto3.client('emr', 
                          aws_access_key_id=AWS_CONFIG['ACCESS_KEY'],
                          aws_secret_access_key=AWS_CONFIG['SECRET_KEY'],
                          region_name='eu-west-3')

class JobRequestSchema(Schema):
    """Schema for validating job request data."""
    job_name = fields.Str(required=True)
    step = fields.Str(required=True)

def validate_request(schema):
    """Decorator to validate request data against a schema."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                schema().load(request.json)
            except ValidationError as err:
                return jsonify({"error": "Invalid input", "details": err.messages}), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_api_key(func):
    """Decorator to check for valid API key in request headers."""
    @wraps(func)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-Api-Key')
        if api_key and api_key == API_SECRET:
            return func(*args, **kwargs)
        return jsonify({'error': 'Unauthorized'}), 401
    return decorated

@app.route('/api/v1/emr/job/start', methods=['POST'])
@require_api_key
@validate_request(JobRequestSchema)
def start_emr_job():
    """
    Start a new EMR job.
    
    Expected JSON payload:
    {
        "job_name": "string",
        "step": "string"
    }
    """
    try:
        data = request.json
        job_name = data['job_name']
        step = data['step']

        step_config = create_step_config(job_name, step)
        response = emr_client.add_job_flow_steps(
            JobFlowId=EMR_CONFIG['CLUSTER_ID'],
            Steps=[step_config]
        )

        return jsonify({'success': True, 'step_id': response['StepIds'][0]})
    except boto3.exceptions.Boto3Error as e:
        return jsonify({'error': 'AWS EMR error', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Unexpected error', 'details': str(e)}), 500

def create_step_config(job_name, step):
    """Create the configuration for an EMR step."""
    return {
        'Name': job_name,
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                'bash',
                '-c',
                f'cd /home/hadoop/ && '
                f'aws s3 sync {EMR_CONFIG["S3_PATH"]}/{step}/ /home/hadoop/{step}/ && '
                f'cd /home/hadoop/{step} && '
                'spark-submit --conf spark.pyspark.python=/home/hadoop/myenv/bin/python '
                '--py-files dependencies.py job.py'
            ]
        }
    }

@app.errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request errors."""
    return jsonify({'error': 'Bad Request', 'details': str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    return jsonify({'error': 'Not Found', 'details': 'The requested URL was not found on the server.'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 Method Not Allowed errors."""
    return jsonify({'error': 'Method Not Allowed', 'details': 'The method is not allowed for the requested URL.'}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)