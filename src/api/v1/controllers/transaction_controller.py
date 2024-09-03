from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.api.v1.schemas.transaction_schema import TransferSchema, WithdrawDepositSchema
from src.services.transaction_service import TransactionService
from extensions import db


transaction_bp = Blueprint("transaction", __name__)


@transaction_bp.put('/transfer')
@jwt_required()
def transfer():
    """
    ---
    tags:
      - Transaction
    summary: Transfer transaction
    description: Transfer funds to another user account
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Respond with **'Bearer &lt;JWT&gt;'**, where JWT is the access token.
      - name: id
        in: formData
        type: integer
        required: true
        description: The account ID of the sender.
      - name: receiver_username
        in: formData
        type: string
        required: true
        description: The username of the receiver.
      - name: receiver_id
        in: formData
        type: integer
        required: true
        description: The account ID of the receiver.
      - name: amount
        in: formData
        type: number
        required: true
        description: The amount to transfer.
    security:
      - BearerAuth: []
    responses:
      200:
        description: Successful transfer from sender to receiver.
      401:
        description: Input data validation error or unauthorized token.
      402:
        description: Invalid transfer request.
      404:
        description: User or Account not found error.
    """
    schema = TransferSchema()
    try:
        data = schema.load(request.form)
    except ValidationError as e:
        return jsonify(e.messages), 401
    
    username = get_jwt_identity()
    transaction_service = TransactionService(db_session=db.session)
    result, status = transaction_service.transfer(data, username)

    return jsonify(result), status

@transaction_bp.put('/deposit')
@jwt_required()
def deposit():
    """
    ---
    tags:
      - Transaction
    summary: Deposit transaction
    description: Deposit funds into an account
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Respond with **'Bearer &lt;JWT&gt;'**, where JWT is the access token.
      - name: id
        in: formData
        type: integer
        required: true
        description: The account ID to deposit funds into.
      - name: amount
        in: formData
        type: number
        required: true
        description: The amount to deposit.
    security:
      - BearerAuth: []
    responses:
      200:
          description: Successful deposit of funds to account.
      401:
        description: Input data validation error or unauthorized token.
      404:
          description: User or Account not found.
    """
    schema = WithdrawDepositSchema()
    try:
        data = schema.load(request.form)
    except ValidationError as e:
        return jsonify(e.messages), 401
    
    username = get_jwt_identity()
    transaction_service = TransactionService(db_session=db.session)
    result, status = transaction_service.deposit(data, username)

    return jsonify(result), status

@transaction_bp.put('/withdraw')
@jwt_required()
def withdraw():
    """
    ---
    tags:
      - Transaction
    summary: Withdraw transaction
    description: Withdraw funds from an account
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Respond with **'Bearer &lt;JWT&gt;'**, where JWT is the access token.
      - name: id
        in: formData
        type: integer
        required: true
        description: The account ID to withdraw funds from.
      - name: amount
        in: formData
        type: number
        required: true
        description: The amount to withdraw.
    security:
      - BearerAuth: []
    responses:
      200:
          description: Successful withdrawal of funds from account.
      401:
        description: Input data validation error or unauthorized token.
      402:
          description: Insufficient funds.
      404:
          description: User or Account not found.            
    """
    schema = WithdrawDepositSchema()
    try:
        data = schema.load(request.form)
    except ValidationError as e:
        return jsonify(e.messages), 401
    
    username = get_jwt_identity()
    transaction_service = TransactionService(db_session=db.session)
    result, status = transaction_service.withdraw(data, username)

    return jsonify(result), status
