from flask import request, jsonify, make_response
from .errors import ERRORS, get_custom_error
from .model import User as UserModel

def check_token_based_authentication():
    # get the auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            return make_response(jsonify(ERRORS['MalformeBearerToken']), 401)
    else:
        auth_token = ''
    if auth_token:
        resp = UserModel.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            request.token = resp
            return
        return make_response(jsonify(get_custom_error(resp)), 401)
    else:
        return make_response(jsonify(ERRORS['InvalidToken']), 401)
