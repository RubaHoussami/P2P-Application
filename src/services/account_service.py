from datetime import datetime

from logger import logger
from src.models.account_model import Account
from src.models.user_model import User
from src.services.user_service import UserService
from src.utils.constants import currency_map, TransactionType


class AccountService():
    def __init__(self, db_session):
        self.db_session = db_session
        self.user_service = UserService(db_session)
    
    def get_account_from_user(self, user: User, id: str) -> Account:
        account = user.accounts.filter_by(id=id).first()
        if account and account.active:
            return account
        return None
    
    def create(self, data: dict, username: str) -> dict:
        currency = data['currency']

        logger.info('User creating account')

        user = self.user_service.get_user_by_username(username)

        if not user:
            return {'error': 'User not found'}, 404
        
        user_id = user.id
        date = datetime.now()

        account = Account(user_id=user_id, currency=currency, date=date)

        self.db_session.add(account)
        self.db_session.commit()

        logger.info('Account created successfully')

        return {'message': 'Account created successfully', 'account id': account.id}, 200

    def delete(self, data: dict, username: str) -> dict:
        id = data['id']

        logger.info('User deleting account')

        user = self.user_service.get_user_by_username(username)

        if not user:
            return {'error': 'User not found'}, 404
        
        account = self.get_account_from_user(user, id)
        
        if not account:
            return {'error': 'Account not found'}, 404
        
        if account.balance != 0:
            return {'error': 'Please withdraw all funds before deleting account', 'account id': account.id}, 402
        
        account.active = False
        self.db_session.commit()

        logger.info('Account deleted successfully')

        return {'message': 'Account deleted successfully'}, 200
    
    def balance(self, data: dict, username:str) -> dict:
        id = data['id']

        logger.info('User checking account balance')

        user = self.user_service.get_user_by_username(username)

        if not user:
            return {'error': 'User not found'}, 404
        
        account = self.get_account_from_user(user, id)
        
        if not account:
            return {'error': 'Account not found'}, 404
        
        logger.info('Account balance retrieved successfully')
        
        return {'message': 'Account balance retrieved successfully', 'account': {'id': account.id, 'balance': account.balance, 'currency': currency_map.get(account.currency)}}, 200
    
    def get_transactions(self, account: Account) -> list[dict]:
        transactions = account.transactions_sent.all() + account.transactions_received.all()
        transactions = {transaction.id: transaction for transaction in transactions}
        transactions_view = []

        for transaction_id in transactions:
            transaction = transactions[transaction_id]
            match transaction.type:
                case TransactionType.TRANSFER.value:
                    transactions_view.append({'type': 'transfer', 'amount': transaction.amount, 'transaction date': transaction.date, 'sender': transaction.sender_account.user.username, 'sender account id': transaction.sender_account.id, 'receiver': transaction.receiver_account.user.username, 'receiver account id': transaction.receiver_account.id})
                case TransactionType.DEPOSIT.value:
                    transactions_view.append({'type': 'deposit', 'amount': transaction.amount, 'transaction date': transaction.date, 'account id': transaction.receiver_account.id})
                case TransactionType.WITHDRAW.value:
                    transactions_view.append({'type': 'withdraw', 'amount': transaction.amount, 'transaction date': transaction.date, 'account id': transaction.receiver_account.id})
                case _:
                    raise ValueError(f'Invalid transaction type: {transaction.type}')
                
        transactions_view.sort(key=lambda x: x['transaction date'], reverse=True)
        return transactions_view

    def transaction_history(self, data: dict, username: str) -> dict:
        id = data['id']

        logger.info('User viewing transaction history')

        user = self.user_service.get_user_by_username(username)

        if not user:
            return {'error': 'User not found'}, 404
        
        account = self.get_account_from_user(user, id)
        
        if not account:
            return {'error': 'Account not found'}, 404
        
        transactions_view = self.get_transactions(account)

        logger.info('Transaction history retrieved successfully')

        return {'message': 'Transaction history retrieved successfully', 'transactions': transactions_view}, 200
    
    def all_transaction_history(self, username: str) -> dict:
        logger.info('User viewing all transaction history')

        user = self.user_service.get_user_by_username(username)

        if not user:
            return {'error': 'User not found'}, 404
        
        transactions_view = []
        for account in user.accounts:
            transactions_view.extend(self.get_transactions(account))

        logger.info('All transaction history retrieved successfully')

        return {'message': 'All transaction history retrieved successfully', 'transactions': transactions_view}, 200