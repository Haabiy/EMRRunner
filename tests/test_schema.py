import pytest
from marshmallow import ValidationError
from app.schema import JobRequestSchema

def test_valid_schema():
    schema = JobRequestSchema()
    valid_data = {"job_name": "test_job", "step": "test_step"}
    result = schema.load(valid_data)
    assert result == valid_data

def test_invalid_schema():
    schema = JobRequestSchema()
    invalid_data = {"job_name": "test_job"}
    with pytest.raises(ValidationError):
        schema.load(invalid_data)
