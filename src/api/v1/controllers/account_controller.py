from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.api.v1.schemas.account_schema import CreateAccountSchema, AccountSchema
from src.services.account_service import AccountService
from extensions import db


account_bp = Blueprint("account", __name__)


@account_bp.put('/create')
@jwt_required()
def create():
    """
    ---
    tags:
      - Account
    summary: Create a new account
    description: Creates a new account for the user with the specified currency.
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Respond with **'Bearer &lt;JWT&gt;'**, where JWT is the access token.
      - name: currency
        in: formData
        type: string
        required: true
        description: The currency for the account (either LBP or USD).
    security:
      - BearerAuth: []
    responses:
      200:
        description: Successful account creation.
      401:
        description: Input data validation error or unauthorized token.
      404:
        description: User not found error.
    """
    schema = CreateAccountSchema()
    try:
        data = schema.load(request.form)
    except ValidationError as e:
        return jsonify(e.messages), 401
    
    username = get_jwt_identity()
    account_service = AccountService(db_session=db.session)
    result, status = account_service.create(data, username)

    return jsonify(result), status

@account_bp.post('/balance')
@jwt_required()
def balance():
    """
    ---
    tags:
      - Account
    summary: Retrieve account balance
    description: Retrieves the balance for a specific account.
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
        description: The ID of the account to retrieve the balance for.
    security:
      - BearerAuth: []
    responses:
      200:
        description: Successful retrieval of account balance.
      401:
        description: Input data validation error or unauthorized token.
      404:
        description: User or Account not found error.
    """
    schema = AccountSchema()
    try:
        data = schema.load(request.form)
    except ValidationError as e:
        return jsonify(e.messages), 401
    
    username = get_jwt_identity()
    account_service = AccountService(db_session=db.session)
    result, status = account_service.balance(data, username)

    return jsonify(result), status

@account_bp.get('/view-transaction-history')
@jwt_required()
def transaction_history():
    """
    ---
    tags:
      - Account
    summary: View account transaction history
    description: Retrieves the transaction history for a specific account.
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
        description: The ID of the account to retrieve the transaction history for.
    security:
      - BearerAuth: []
    responses:
      200:
        description: Successful retrieval of transaction history for the account.
      401:
        description: Input data validation error or unauthorized token.
      404:
        description: User or Account not found error.
    """
    schema = AccountSchema()
    try:
        data = schema.load(request.form)
    except ValidationError as e:
        return jsonify(e.messages), 401
    
    username = get_jwt_identity()
    account_service = AccountService(db_session=db.session)
    result, status = account_service.transaction_history(data, username)

    return jsonify(result), status

@account_bp.get('/view-all-transaction-history')
@jwt_required()
def view_accounts():
    """
    ---
    tags:
      - Account
    summary: View all transaction history
    description: Retrieves the transaction history for all accounts associated with the user.
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Respond with **'Bearer &lt;JWT&gt;'**, where JWT is the access token.
    security:
      - BearerAuth: []
    responses:
      200:
        description: Successful retrieval of all transaction histories for all the user's accounts.
      404:
        description: User not found error.
    """
    username = get_jwt_identity()
    account_service = AccountService(db_session=db.session)
    result, status = account_service.all_transaction_history(username)
    return jsonify(result), status

@account_bp.delete('/delete')
@jwt_required()
def delete():
    """
    ---
    tags:
      - Account
    summary: Delete an account
    description: Deletes a specific account for the user.
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
        description: The ID of the account to delete.
    security:
      - BearerAuth: []
    responses:
      200:
        description: Successful account deletion.
      401:
        description: Input data validation error or unauthorized token.
      402:
        description: Error during account deletion.
      404:
        description: User or Account not found error.
    """
    schema = AccountSchema()
    try:
        data = schema.load(request.form)
    except ValidationError as e:
        return jsonify(e.messages), 401
    
    username = get_jwt_identity()
    account_service = AccountService(db_session=db.session)
    result, status = account_service.delete(data, username)

    return jsonify(result), status
