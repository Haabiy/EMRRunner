from flask import Flask, request, jsonify
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# AWS credentials and region
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')

# EMR configurations
EMR_CLUSTER_ID = os.getenv('EMR_CLUSTER_ID')
S3_BUCKET = os.getenv('BUCKET_NAME')
API_KEY_VALUE = os.getenv('API_KEY_VALUE')

# Boto3 EMR client
emr_client = boto3.client('emr', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)

def check_api_key():
    apikey = request.headers.get('apikey')
    return apikey == API_KEY_VALUE

@app.route('/start_emr_job', methods=['POST'])
def start_emr_job():
    try:
        if not check_api_key():
            return jsonify({'success': False, 'error': 'Unauthorized, missing or mismatching apikey'}), 403
        
        # Get job name from the request
        job_name = request.json.get('job_name')
        step = request.json.get('step')
        s3_path = os.getenv("S3_PATH")
        #### SIMPLE STEP
        step_config = {
            'Name': job_name,
            'ActionOnFailure': 'CONTINUE',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': [
                    'bash',
                    '-c',
                    'source /home/hadoop/myenv/bin/activate && '  # Activate the virtual environment
                    'cd /home/hadoop/ && ' 
                    f'aws s3 sync {s3_path}/{step}/ /home/hadoop/{step}/ && '
                    f'cd /home/hadoop/{step} && '
                    'spark-submit --deploy-mode cluster --conf spark.pyspark.python=/usr/bin/python3 --py-files job.py Testjob.py '
                ] 
            }
        }

        # Add the step to the EMR cluster
        response = emr_client.add_job_flow_steps(
            JobFlowId=EMR_CLUSTER_ID,
            Steps=[step_config]
        )
        #print(response)
        return jsonify({'success': True, 'step_id': response['StepIds'][0]})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/check_job_status', methods=['POST'])
def check_job_status():
    try:
        if not check_api_key():
            return jsonify({'success': False, 'error': 'Unauthorized, missing or mismatching apikey'}), 403

        # Get the job ID from reqyest object
        step_id = request.json.get('step_id')
        # Get the status of the EMR job step
        response = emr_client.describe_step(ClusterId=EMR_CLUSTER_ID, StepId=step_id)
        status = response['Step']['Status']['State']

        return jsonify({'success': True, 'status': status})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
@app.route('/check_cluster_status', methods=['POST'])
def check_cluster_status():
    try:
        if not check_api_key():
            return jsonify({'success': False, 'error': 'Unauthorized, missing or mismatching apikey'}), 403

        # Get the status of the EMR cluster
        response = emr_client.describe_cluster(ClusterId=EMR_CLUSTER_ID)
        status = response['Cluster']['Status']['State']

        return jsonify({'success': True, 'status': status})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)