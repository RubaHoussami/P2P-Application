from extensions import db
from src.utils.constants import Currency

class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)

    transactions_sent = db.relationship('Transaction', foreign_keys='Transaction.sender_id', backref='sender_account', lazy='dynamic')
    transactions_received = db.relationship('Transaction', foreign_keys='Transaction.receiver_id', backref='receiver_account', lazy='dynamic')

    currency = db.Column(db.Integer, nullable=False, default=Currency.LBP.value)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    date = db.Column(db.DateTime, nullable=False)
