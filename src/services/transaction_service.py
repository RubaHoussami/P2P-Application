from datetime import datetime

from logger import logger
from src.models.transaction_model import Transaction
from src.services.account_service import AccountService
from src.services.user_service import UserService
from src.utils.constants import TransactionType


class TransactionService():
    def __init__(self, db_session):
        self.db_session = db_session
        self.account_service = AccountService(db_session)
        self.user_service = UserService(db_session)

    def get_transaction(self, id: str) -> Transaction:
        return self.db_session.query(Transaction).filter_by(id=id).first()
    
    def transfer(self, data: dict, username: str) -> dict: 
        id = data['id']
        receiver_username = data['receiver_username']
        receiver_id = data['receiver_id']
        amount = data['amount']

        logger.info('User transferring funds')

        if id == receiver_id or username == receiver_username:
            return {'error': 'Cannot transfer to self'}, 402
        
        user = self.user_service.get_user_by_username(username)
        receiver_user = self.user_service.get_user_by_username(receiver_username)
        if not user:
            return {'error': 'User not found'}, 404
        if not receiver_user:
            return {'error': 'Receiver not found'}, 404
    
        account = self.account_service.get_account_from_user(user, id)
        receiver = self.account_service.get_account_from_user(receiver_user, receiver_id)
        if not account:
            return {'error': 'Account not found'}, 404
        if not receiver:
            return {'error': 'Receiver account not found'}, 404
        
        if account.currency != receiver.currency:
            return {'error': 'Currency mismatch'}, 402
        if account.balance < amount:
            return {'error': 'Insufficient funds'}, 402
        
        account.balance -= amount
        receiver.balance += amount
        date = datetime.now()

        transaction = Transaction(type=TransactionType.TRANSFER.value, sender_id=id, receiver_id=receiver_id, amount=amount, date=date)

        self.db_session.add(transaction)
        self.db_session.commit()

        logger.info('Transfer successful')

        return {'message': 'Transfer successful'}, 200
    
    def deposit(self, data: dict, username: str) -> dict:
        id = data['id']
        amount = data['amount']

        logger.info('User depositing funds')

        user = self.user_service.get_user_by_username(username)
        if not user:
            return {'error': 'User not found'}, 404
    
        account = self.account_service.get_account_from_user(user, id)
        if not account:
            return {'error': 'Account not found'}, 404
        
        account.balance += amount
        date = datetime.now()

        transaction = Transaction(type=TransactionType.DEPOSIT.value, sender_id=id, receiver_id=id, amount=amount, date=date)

        self.db_session.add(transaction)
        self.db_session.commit()

        logger.info('Deposit successful')

        return {'message': 'Deposit successful'}, 200
    
    def withdraw(self, data: dict, username: str) -> dict:
        id = data['id']
        amount = data['amount']

        logger.info('User withdrawing funds')

        user = self.user_service.get_user_by_username(username)
        if not user:
            return {'error': 'User not found'}, 404
        
        account = self.account_service.get_account_from_user(user, id)
        if not account:
            return {'error': 'Account not found'}, 404
        
        if account.balance < amount:
            return {'error': 'Insufficient funds'}, 402
        
        account.balance -= amount
        date = datetime.now()

        transaction = Transaction(type=TransactionType.WITHDRAW.value, sender_id=id, receiver_id=id, amount=amount, date=date)

        self.db_session.add(transaction)
        self.db_session.commit()

        logger.info('Withdrawal successful')

        return {'message': 'Withdrawal successful'}, 200
