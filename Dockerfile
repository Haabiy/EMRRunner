# Dockerfile
FROM python:3.12

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "app/emr_job_api.py"]
