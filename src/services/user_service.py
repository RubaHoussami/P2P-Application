from datetime import datetime
import hashlib
import secrets
from flask_jwt_extended import create_access_token, create_refresh_token

from logger import logger
from src.models.user_model import User
from src.models.token_blocklist_model import TokenBlocklist
from src.utils.constants import currency_map


class UserService():
    def __init__(self, db_session):
        self.db_session = db_session

    def salt_and_hash(self, password: str) -> tuple[str, str]:
        '''
        Function to generate a salt and hash a password
        '''
        salt = secrets.token_hex(16)
        hash_object = hashlib.sha256((password + salt).encode())
        hash_hex = hash_object.hexdigest()
        return salt, hash_hex

    def authenticate_user(self, password: str, salt: str, hash_hex: str) -> bool:
        '''
        Function to authenticate a user through hashing and salting the given password and comparing it to the stored hash
        '''
        hash_object = hashlib.sha256((password + salt).encode())
        hash_hex_check = hash_object.hexdigest()
        return hash_hex == hash_hex_check

    def get_user_by_username(self, username:str) -> User:
        user = self.db_session.query(User).filter_by(username=username).first()
        if user and user.active:
            return user
        return None

    def get_user_by_email(self, email: str) -> User:
        user = self.db_session.query(User).filter_by(email=email).first()
        if user and user.active:
            return user
        return None
    
    def get_user(self, username: str, email: str) -> User:
        if username:
            return self.get_user_by_username(username)
        return self.get_user_by_email(email.lower())
    
    def create_response(self, username: str, message: str) -> dict:
        access = create_access_token(identity=username, fresh=True)
        refresh = create_refresh_token(identity=username)
        return {'user': {'access': access, 'refresh': refresh}, 'message': message}, 200

    def login(self, data: dict) -> dict:
        username = data.get('username')
        email = data.get('email')
        password = data['password']

        logger.info('User logging in')
        
        user = self.get_user(username, email)
        if not user:
            return {'error': 'User not found'}, 404
        
        valid = self.authenticate_user(password, user.salt, user.password)

        if not valid:
            return {'error': 'Invalid username or password'}, 402
        
        logger.info('User logged in successfully')

        return self.create_response(user.username, 'User logged in successfully')

    def register(self, data: dict) -> dict:
        username = data['username']
        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']
        password = data['password']

        logger.info('User registering')

        if self.get_user(username, email):
            return {'error': 'Username or email already exists'}, 402
        
        date = datetime.now()
        salt, hash_hex = self.salt_and_hash(password)

        user = User(first_name=first_name, last_name=last_name, username=username, email=email.lower(), password=hash_hex, salt=salt, date=date)

        self.db_session.add(user)
        self.db_session.commit()

        logger.info('User registered successfully')
        
        return self.create_response(username, 'User registered successfully')
    
    def update(self, data: dict, username: str) -> dict:
        logger.info('User updating information')

        user = self.get_user_by_username(username)

        if not user:
            return {'error': 'User not found'}, 404
        
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        new_password = data.get('new_password')
        
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if new_password:
            salt, hash_hex = self.salt_and_hash(new_password)
            user.password = hash_hex
            user.salt = salt

        self.db_session.commit()

        logger.info('User updated successfully')

        return {'message': 'User information updated successfully'}, 200
    
    def profile(self, username: str) -> dict:
        logger.info('User viewing profile')

        user = self.get_user_by_username(username)

        if not user:
            return {'error': 'User not found'}, 404
        
        user_view = {'username': user.username, 'email': user.email, 'first name': user.first_name, 'last name': user.last_name, 'date created': user.date}
        
        logger.info('User profile viewed successfully')

        return {'message': 'User retreived successfully', 'user': user_view}, 200
    
    def view_accounts(self, username: str) -> dict:
        logger.info('User viewing accounts')

        user = self.get_user_by_username(username)

        if not user:
            return {'error': 'User not found'}, 404
        
        accounts = user.accounts.all()
        if not accounts:
            return {'message': 'No accounts found'}, 200
        
        accounts_view = [{'id': account.id, 'currency': currency_map.get(account.currency), 'balance': account.balance, 'date created': account.date} for account in accounts]

        logger.info('Accounts viewed successfully')

        return {'message': 'Accounts retreived successfully','accounts': accounts_view}, 200

    def delete(self, username:str) -> dict:
        logger.info('Deleting user')

        user = self.get_user_by_username(username)

        if not user:
            return {'error': 'User not found'}, 404
        
        for account in user.accounts:
            if account.balance != 0:
                return {'error': 'Please withdraw all funds before deleting account', 'account id': account.id}, 402
        
        for account in user.accounts:
            account.active = False
        
        user.active = False
        self.db_session.commit()

        logger.info('User deleted successfully')

        return {'message': 'User deleted successfully'}, 200
    
    def logout(self, username: str, jti: str) -> dict:
        logger.info('Logging out user')

        user = self.get_user_by_username(username)

        if not user:
            return {'error': 'User not found'}, 404
        
        date = datetime.now()
        token = TokenBlocklist(jti=jti, date=date)
        self.db_session.add(token)
        self.db_session.commit()

        logger.info('User logged out successfully')
        
        return {'message': 'User logged out successfully'}, 200
    
    def refresh(self, username: str, jti: str) -> dict:
        logger.info('Refreshing token')

        user = self.get_user_by_username(username)

        if not user:
            return {'error': 'User not found'}, 404
        
        date = datetime.now()
        token = TokenBlocklist(jti=jti, date=date)
        self.db_session.add(token)
        self.db_session.commit()

        logger.info('Token refreshed successfully')

        return self.create_response(username, 'Token refreshed successfully')
