from marshmallow import Schema, fields, validate, validates_schema
from .validators import validate_password, validate_email, validate_credentials

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True, validate=validate_email)
    password = fields.Str(load_only=True, required=True,
                          validate=[
                              validate.Length(min=8),
                              validate_password
                              ]
                          )

class LoginSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3))
    password = fields.Str(required=True)
    
    @validates_schema
    def validate_user(self, data, **kwargs):
        validate_credentials(data)
    
user_schema = UserSchema()
login_schema = LoginSchema()
