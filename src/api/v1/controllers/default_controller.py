from flask import Blueprint, jsonify

from logger import logger


default_bp = Blueprint("default", __name__)


@default_bp.route('/')
def default():
    """
    ---
    tags:
      - Default
    summary: Default route
    description: This is the default route.
    responses:
      200:
        description: Default route response
    """
    logger.info('Deafult router accessed')
    return jsonify({'message': 'Application up and running'}), 200
