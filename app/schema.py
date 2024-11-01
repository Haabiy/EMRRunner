from marshmallow import Schema, fields, validate

class JobRequestSchema(Schema):
    """Schema for validating job request data."""
    job_name = fields.Str(required=True)
    step = fields.Str(required=True)
    deploy_mode = fields.Str(
        load_default='client',  # Use load_default instead of default
        validate=validate.OneOf(['client', 'cluster'])
    )