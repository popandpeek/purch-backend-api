# from datetime import datetime
# from flask import jsonify
# from extensions.api import Blueprint, SQLCursorPage
# from flask_jwt_extended import create_access_token, decode_token
# from flask.views import MethodView
# from schema import LoginQueryArgsSchema, JWTSchema
#
#
# blp = Blueprint('auth', __name__, url_prefix='/login', description="Auth for token JWT")
#
#
# @blueprint_login.route('/')
# class Login(MethodView):
#     @blueprint_login.arguments(LoginQueryArgsSchema, location='query')
#     @blueprint_login.response(200, JWTSchema)
#     def post(self, args):
#         """
#         Get JWT Token
#         """
#         username = args.pop('username', None)
#         access_token = create_access_token(identity=username)
#         pure_decoded = decode_token(access_token)
#         return jsonify(access_token=access_token,
#                        token_type='Bearer',
#                        expires=datetime.fromtimestamp(pure_decoded["exp"]).strftime('%Y-%m-%d %H:%M:%S')), 200
