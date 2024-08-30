from marshmallow import Schema, fields, validate
from src.utils.constants import Currency

class CreateAccountSchema(Schema):
    currency = fields.String(required = True, validate = validate.OneOf([currency.name for currency in Currency]))

class AccountSchema(Schema):
    id = fields.Integer(required = True)
