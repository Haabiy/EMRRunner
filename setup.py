from setuptools import setup, find_packages

with open("README.md", "r") as README:
    description = README.read()

setup(
    name='emrrunner',
    version='v1.0.0',
    packages=['app'],
    include_package_data=True,
    install_requires=[
        'Flask',
        'boto3',
        'python-dotenv',
        'marshmallow',
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'emrrunner=app.cli:cli_main',
        ],
    },
    long_description=description,
    long_description_content_type="text/markdown"
)