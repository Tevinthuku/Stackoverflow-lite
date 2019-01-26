import os
import datetime
import jwt

from flask import request, jsonify, make_response, abort
from werkzeug.security import generate_password_hash, check_password_hash
from app.api.v1.model import UserModel, USERS
from app.api.v1 import path_1
from app.utils import validate_email, check_password, is_user_admin

key = os.getenv('SECRET_KEY', default="BIG-SECRET")


@path_1.route("/auth/signup", methods=['POST'])
def user_sign_up():
    try:
        firstname = request.get_json()['firstname']
        lastname = request.get_json()['lastname']
        username = request.get_json()['username']
        email = request.get_json()['email']
        password = request.get_json()['password']
        confirm_pass = request.get_json()['confirm_password']
        is_admin = is_user_admin(username)

    except KeyError:
        abort(make_response(jsonify({'status': 400,
                                     'error': "Please check your json keys and try again"}), 400))

    # this 2 checks will throw an exception if none
    # of their requirements are met.
    check_password(password, confirm_pass)
    email = validate_email(email)

    user = UserModel(firstname=firstname,
                     username=username,
                     lastname=lastname,
                     email=email,
                     password=password, is_admin=is_admin)

    # call the save_user method from the models
    user.save_user()
    return jsonify({"status": 201, "data": "User Registered Successfully!"}), 201

# login route


@path_1.route("/auth/login", methods=['POST'])
def user_login():

    try:
        username = request.get_json()['username']
        password = request.get_json()['password']

    except KeyError:
        abort(make_response(jsonify({'status': 400,
                                     ' error': "Check your json keys and try again. Make sure it is username and password"}), 400))

    user = UserModel.query_users(username, password)
    if not user:
        return jsonify({"status": 400, "data": "Please Register First to Login"}), 400

    token = jwt.encode({"username": username}, key, algorithm='HS256')
    return jsonify({"status": 200, "token": token.decode('UTF-8'), "message": "You have Logged in Successfully"}), 200
