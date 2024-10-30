from marshmallow import Schema, fields

class JobRequestSchema(Schema):
    """Schema for validating job request data."""
    job_name = fields.Str(required=True)
    step = fields.Str(required=True)
