from extensions import db
from src.utils.constants import TransactionType

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    type = db.Column(db.String(100), nullable=False, default=TransactionType.TRANSFER.value)

    sender_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)

    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
