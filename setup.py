from setuptools import setup, find_packages

setup(
    name='app',
    version='v1.0.2',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'boto3',
        'python-dotenv',
        'marshmallow',
    ],
    entry_points={
        'console_scripts': [
            'run-my-emr-api=app.emr_job_api:run_app',
        ],
    },
)
