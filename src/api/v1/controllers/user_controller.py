from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token, get_jwt

from src.api.v1.schemas.user_schema import UserLoginSchema, UserRegisterSchema, UserUpdateSchema
from src.services.user_service import UserService
from extensions import db


user_bp = Blueprint("user", __name__)


@user_bp.post('/login')
def login():
    """
    ---
    tags:
      - User
    summary: User login
    description: Authenticates the user using the provided username or email and password, and returns JWT access and refresh tokens upon successful authentication.
    parameters:
      - name: username
        in: formData
        type: string
        description: The username of the user. This field is required if email is not provided.
      - name: email
        in: formData
        type: string
        format: email
        description: The email of the user. This field is required if username is not provided.
      - name: password
        in: formData
        type: string
        required: true
        description: The user's password.
    responses:
      200:
        description: Successful login, returns JWT access and refresh tokens.
      401:
        description: Input data validation error or unauthorized token.
      402:
        description: Invalid username or password error.
      404:
        description: User not found error.
    """
    schema = UserLoginSchema()
    try:
        data = schema.load(request.form)
    except ValidationError as e:
        return jsonify(e.messages), 401
    
    user_service = UserService(db_session=db.session)
    result, status = user_service.login(data)

    return jsonify(result), status

@user_bp.post('/register')
def register():
    """
    ---
    tags:
      - User
    summary: User registration
    description: Registers a new user with provided details. 
    parameters:
      - name: first_name
        in: formData
        type: string
        required: true
        description: The user's first name.
      - name: last_name
        in: formData
        type: string
        required: true
        description: The user's last name.
      - name: username
        in: formData
        type: string
        required: true
        description: The username of the user.
      - name: email
        in: formData
        type: string
        format: email
        required: true
        description: The email of the user.
      - name: password
        in: formData
        type: string
        required: true
        description: The user's password.
      - name: confirm_password
        in: formData
        type: string
        required: true
        description: The user's password confirmation.
    responses:
      200:
        description: Successful registration, returns access and refresh tokens.
      401:
        description: Input data validation error or unauthorized token.
      402:
        description: User already exists error.
    """
    schema = UserRegisterSchema()
    try:
        data = schema.load(request.form)
    except ValidationError as e:
        return jsonify(e.messages), 401
    
    user_service = UserService(db_session=db.session)
    result, status = user_service.register(data)
    
    return jsonify(result), status

@user_bp.put('/update')
@jwt_required()
def update():
    """
    ---
    tags:
      - User
    summary: Update user information
    description: Updates the user's first name, last name, or password.
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Respond with **'Bearer &lt;JWT&gt;'**, where JWT is the access token.
      - name: first_name
        in: formData
        type: string
        description: The user's first name.
      - name: last_name
        in: formData
        type: string
        description: The user's last name.
      - name: new_password
        in: formData
        type: string
        description: The user's new password.
      - name: confirm_new_password
        in: formData
        type: string
        description: The user's new password confirmation.
    security:
      - BearerAuth: []
    responses:
      200:
        description: Successful update of user information.
      401:
        description: Input data validation error or unauthorized token.
      404:
        description: User not found error.
    """
    schema = UserUpdateSchema()
    try:
        data = schema.load(request.form)
    except ValidationError as e:
        return jsonify(e.messages), 401
    
    username = get_jwt_identity()
    user_service = UserService(db_session=db.session)
    result, status = user_service.update(data, username)
    
    return jsonify(result), status

@user_bp.get('/view-profile')
@jwt_required()
def profile():
    """
    ---
    tags:
      - User
    summary: View user profile
    description: Retrieves the profile information of the logged-in user.
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
        description: Successful retrieval of user profile.
      404:
        description: User not found error.
    """
    username = get_jwt_identity()
    user_service = UserService(db_session=db.session)
    result, status = user_service.profile(username)
    return jsonify(result), status

@user_bp.get('/view-accounts')
@jwt_required()
def view_accounts():
    """
    ---
    tags:
      - User
    summary: View user accounts
    description: Retrieves all accounts associated with the logged-in user.
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
        description: Successful retrieval of user accounts information.
      404:
        description: User not found error.
    """
    username = get_jwt_identity()
    user_service = UserService(db_session=db.session)
    result, status = user_service.view_accounts(username)
    return jsonify(result), status

@user_bp.delete('/delete')
@jwt_required()
def delete():
    """
    ---
    tags:
      - User
    summary: Delete user account
    description: Deactivates the user account after ensuring all associated accounts have a zero balance.
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
        description: Successful user deletion with account deletions as well.
      402:
        description: Error due to non-zero account balances.
      404:
        description: User not found error.
    """
    username = get_jwt_identity()
    user_service = UserService(db_session=db.session)
    result, status = user_service.delete(username)
    return jsonify(result), status

@user_bp.delete('/logout')
@jwt_required()
def logout():
    """
    ---
    tags:
      - User
    summary: User logout
    description: Logs out the user by adding their token to the blocklist.
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
        description: Successful logout message.
      404:
        description: User not found error.
    """
    username = get_jwt_identity()
    jti = get_jwt()["jti"]
    user_service = UserService(db_session=db.session)
    result, status = user_service.logout(username, jti)
    return jsonify(result), status

@user_bp.delete('/logout-refresh')
@jwt_required(refresh=True)
def logout_refresh():
    """
    ---
    tags:
      - User
    summary: Logout using refresh token
    description: Logs out the user by adding their refresh token to the blocklist.
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Respond with **'Bearer &lt;JWT&gt;'**, where JWT is the refresh token.
    security:
      - BearerAuth: []
    responses:
      200:
        description: Successful logout message.
      404:
        description: User not found error.
    """
    username = get_jwt_identity()
    jti = get_jwt()["jti"]
    user_service = UserService(db_session=db.session)
    result, status = user_service.logout(username, jti)
    return jsonify(result), status

@user_bp.post('/refresh')
@jwt_required(refresh=True)
def refresh():
    """
    ---
    tags:
      - User
    summary: Refresh access token
    description: Generates a new access token using the refresh token.
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Respond with **'Bearer &lt;JWT&gt;'**, where JWT is the refresh token.
    security:
      - BearerAuth: []
    responses:
      200:
        description: Successful token refresh with new access token.
      404:
        description: User not found error.
    """
    username = get_jwt_identity()
    jti = get_jwt()["jti"]
    user_service = UserService(db_session=db.session)
    result, status = user_service.refresh(username, jti)
    return result, status
