import boto3
from app.config import AWS_CONFIG, EMR_CONFIG

# Initialize Boto3 EMR client
emr_client = boto3.client(
    'emr', 
    aws_access_key_id=AWS_CONFIG['ACCESS_KEY'],
    aws_secret_access_key=AWS_CONFIG['SECRET_KEY'],
    region_name=AWS_CONFIG['REGION']
)

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

def start_emr_job(job_name, step):
    """Function to start an EMR job."""
    step_config = create_step_config(job_name, step)
    response = emr_client.add_job_flow_steps(
        JobFlowId=EMR_CONFIG['CLUSTER_ID'],
        Steps=[step_config]
    )
    return response['StepIds'][0]

