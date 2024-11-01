from flask import Flask, request, jsonify
from app.decorators import require_api_key, validate_request
from app.schema import JobRequestSchema
from app.emr_client import start_emr_job


app = Flask(__name__)

@app.route('/api/v1/emr/job/start', methods=['POST'])
@require_api_key
def start_emr_job_endpoint():
    """
    Start a new EMR job.
    
    Expected JSON payload:
    {
        "job_name": "string",
        "step": "string",
        "deploy_mode": "client|cluster"  # Optional, defaults to "client"
    }
    """
    try:
        data = request.validated_data
        step_id = start_emr_job(
            job_name=data['job_name'],
            step=data['step'],
            deploy_mode=data.get('deploy_mode', 'client')
        )
        
        return jsonify({
            'success': True,
            'step_id': step_id,
            'details': {
                'job_name': data['job_name'],
                'step': data['step'],
                'deploy_mode': data.get('deploy_mode', 'client')
            }
        })
    except Exception as e:
        return jsonify({'error': 'Unexpected error', 'details': str(e)}), 500

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