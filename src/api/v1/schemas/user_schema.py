from marshmallow import Schema, fields, validate, validates_schema, ValidationError

class UserLoginSchema(Schema):
    username = fields.Str()
    email = fields.Email()
    password = fields.Str(required=True, validate=validate.Length(min=1))

    @validates_schema
    def check(self, data, **kwargs):
        if 'email' not in data and 'username' not in data:
            raise ValidationError('Email or username is required')
        if 'email' in data and 'username' in data:
            raise ValidationError('Email and username cannot be both provided')

class UserRegisterSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=1))
    confirm_password = fields.Str(required=True, validate=validate.Length(min=1))

    @validates_schema
    def check(self, data, **kwargs):
        if data['password'] != data['confirm_password']:
            raise ValidationError('Password and confirm password must match')

class UserUpdateSchema(Schema):
    first_name = fields.Str()
    last_name = fields.Str()
    new_password = fields.Str()
    confirm_new_password = fields.Str()

    @validates_schema
    def check(self, data, **kwargs):
        if 'first_name' not in data and 'last_name' not in data and 'new_password' not in data:
            raise ValidationError('At least one field must be updated')
        if 'new_password' in data and 'confirm_new_password' not in data:
            raise ValidationError('Confirm new password is required')
        if 'confirm_new_password' in data and 'new_password' not in data:
            raise ValidationError('New password is required')
        if 'new_password' in data and 'confirm_new_password' in data:
            if data['new_password'] != data['confirm_new_password']:
                raise ValidationError('New password and confirm new password must match')
