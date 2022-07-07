from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, create_access_token
from src.extensions import jwt_manager
from src.model import *

blueprint_users = Blueprint('users_bp', __name__)


@blueprint_users.route('/login', methods=['GET'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message='Login succeeded.', access_token=access_token)
    else:
        return jsonify(message='Entered a bad email/password'), 401