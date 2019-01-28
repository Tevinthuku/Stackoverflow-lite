# This module contains the functions that will validate users data
# imports
import os
import re
from functools import wraps
import jwt
from flask import jsonify, request, abort, make_response
from werkzeug.security import generate_password_hash

# local imports
from app.api.v1.model import UserModel, USERS

key = os.getenv('SECRET_KEY', default="BIG-SECRET")


def abortFn(error):
    abort(make_response(jsonify(
        error=error), 400))


def check_password(password, confirmed_password):
    '''
     Lets check if our passoword meets the requirements
    '''
    # check to confirm the password is of required length
    if len(password) < 8 or len(password) > 20:
        abortFn(
            "Password should not be less than 8 characters or exceed 20")

    # check if password contains at least an alphabet(a-z)
    if not re.search("[a-z]", password):
        abortFn("Password should contain a letter between a-z")

    # check if password contains at least an upper case letter
    if not re.search("[A-Z]", password):
        abortFn("Password should contain a capital letter")

    # check if password contains at least a number(0-9)
    if not re.search("[0-9]", password):
        abortFn("Password should contain a number(0-9)")

    # Checks if passwords provided by the users match
    if password != confirmed_password:
        abortFn("Your passwords don't match!")

    # If they match..
    hashed_password = generate_password_hash(password, method='sha256')

    return hashed_password


# validate email


def validate_email(email):
    """
    Is the email valid , is it already used?
    """

    for user in USERS:
        if email == user.email:
            abortFn("Email is already taken!")
    try:
        user, domain = str(email).split("@")
    except ValueError:
        abortFn("Email is Invalid")
    if not user or not domain:
        abortFn("Email is Invalid")

    # Is the domain you are using valid?
    try:
        dom1, dom2 = domain.split(".")
    except ValueError:
        abortFn("Email is Invalid")
    if not dom1 or not dom2:
        abortFn("Email is Invalid")

    return email

# wrap our function and check for the access-token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': "Token is missing"}), 401

        try:
            data = jwt.decode(token, key=key, algorithms='HS256')
            current_user = None
            VARUSERS = [vars(user) for user in USERS]
            for user in VARUSERS:
                if user.get("username") == data['username']:
                    current_user = user
        except:
            return jsonify({'message': 'The token is expired or invalid'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

# lets decode our token back


def decode_token():
    token = request.headers['x-access-token']
    try:
        username = jwt.decode(token, key)

    except:
        return jsonify({"message": "The token is expired or invalid"}), 401

    return username

# lests verify if the user is an admin or not


def is_user_admin(username):
    return True if username == "Tevinthuku" else False
