from marshmallow import (
    Schema, fields, validate,
    validates_schema, ValidationError
    )
from .validators import (
    validate_password, validate_email,
    validate_credentials, validate_username
    )

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=[validate.Length(min=3),
                                                   validate_username])
    email = fields.Email(required=True, validate=validate_email)
    password = fields.Str(load_only=True, required=True,
                          validate=[validate.Length(min=8),
                                    validate_password])
    confirm_password = fields.Str(required=True)
    recipes = fields.List(fields.Nested('RecipeSchema', exclude=('author',)))
    
    @validates_schema
    def validate_password_match(self, data, **kwargs):
        if data.get('password') != data.get('confirm_password'):
            raise ValidationError("Passwords do not match.", field_name="confirm_password")

class LoginSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3))
    password = fields.Str(required=True)
    
    @validates_schema
    def validate_user(self, data, **kwargs):
        validate_credentials(data)

login_schema = LoginSchema()
