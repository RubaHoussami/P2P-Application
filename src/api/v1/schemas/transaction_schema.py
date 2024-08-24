from marshmallow import Schema, fields

class TransferSchema(Schema):
    id = fields.Integer(required = True)
    receiver_username = fields.String(required = True)
    receiver_id = fields.Integer(required = True)
    amount = fields.Float(required = True)
    
class WithdrawDepositSchema(Schema):
    id = fields.Integer(required = True)
    amount = fields.Float(required = True)
