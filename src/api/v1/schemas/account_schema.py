from marshmallow import Schema, fields, validate
from src.utils.constants import Currency

class CreateAccountSchema(Schema):
    currency = fields.Integer(required = True, validate = validate.OneOf([c.value for c in Currency]))

class AccountSchema(Schema):
    id = fields.Integer(required = True)
