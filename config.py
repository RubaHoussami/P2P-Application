import os
from datetime import timedelta
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
    
        self.APP_NAME = os.getenv('APP_NAME', 'fallback-name')
        self.APP_DESCRIPTION = os.getenv('APP_DESCRIPTION', 'fallback-description')
        self.APP_VERSION = os.getenv('APP_VERSION', 'fallback-version')
        self.FLASK_DEBUG = False
        self.SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'fallback-uri')
        self.JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'fallback-secret-key')
        self.JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 5)))
        self.JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 5)))
        self.JWT_BLOCKLIST_ENABLED = os.getenv('JWT_BLOCKLIST_ENABLED', 'True').lower() in ['true', '1', 't']
        self.JWT_BLOCKLIST_TOKEN_CHECKS = [x for x in os.getenv('JWT_BLOCKLIST_TOKEN_CHECKS', 'access,refresh').split(',')]

class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self.FLASK_DEBUG = True

class ProductionConfig(Config):
    def __init__(self):
        super().__init__()
        self.FLASK_DEBUG = False

class TestingConfig(Config):
    def __init__(self):
        super().__init__()
        self.FLASK_DEBUG = True
        self.TESTING = True
        self.SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_TEST', 'fallback-test-uri')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
