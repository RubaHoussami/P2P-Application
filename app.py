from flask import Flask
import os
from flasgger import Swagger

from extensions import db, jwt, migrate

from src.models.user_model import User
from src.models.account_model import Account
from src.models.transaction_model import Transaction
from src.models.token_blocklist_model import TokenBlocklist

from src.api.v1.controllers.default_controller import default_bp
from src.api.v1.controllers.account_controller import account_bp
from src.api.v1.controllers.transaction_controller import transaction_bp
from src.api.v1.controllers.user_controller import user_bp

from src.services.token_blocklist_service import check_if_token_revoked
from logger import logger
from config import config


def create_app():
    app = Flask(__name__)

    config_name = os.getenv('FLASK_ENV', 'default')
    app.config.from_object(config[config_name]())

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    if config_name != 'testing':
        with app.app_context():
            db.create_all()

    app.register_blueprint(default_bp)
    app.register_blueprint(account_bp, url_prefix = '/account')
    app.register_blueprint(transaction_bp, url_prefix = '/transaction')
    app.register_blueprint(user_bp, url_prefix = '/user')

    jwt.token_in_blocklist_loader(check_if_token_revoked)

    return app

def create_swagger(app):
    config_name = os.getenv('FLASK_ENV', 'default')
    configuration = config[config_name]()

    swagger = Swagger(app, template={
        "info": {
            "title": configuration.APP_NAME,
            "description": configuration.APP_DESCRIPTION,
            "version": configuration.APP_VERSION,
            }
        }
    )
    
    return swagger

if __name__ == '__main__':
    app = create_app()

    swagger = create_swagger(app)

    logger.info('Starting flask application')
    app.run()
