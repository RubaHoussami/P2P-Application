from logger import logger
from extensions import db
from src.models.token_blocklist_model import TokenBlocklist


def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    logger.info('Checking if token is revoked')

    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist).filter_by(jti=jti).first()

    return token is not None
