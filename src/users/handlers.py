from flask import request, jsonify, make_response
from flask_restful import Resource
from .model import db, User as UserModel
from .utils import check_email
from .errors import ERRORS, get_custom_error

class Balance(Resource):
    def get(self):
        user = UserModel.query.filter_by(id=request.token).first()
        if not user:
            return make_response(jsonify(ERRORS['InvalidToken']), 200)
        responseObject = {
            'status': 'success',
            'data': {
                'email': user.email,
                'current_balance': user.balance
            }
        }
        return make_response(jsonify(responseObject), 200)

class SendPayment(Resource):
    def post(self):
        post_data = request.get_json()

        user = UserModel.query.filter_by(id=request.token).first()

        if not user:
            return make_response(jsonify(ERRORS['InvalidToken']), 200)

        if not post_data.get('to') or not post_data.get('amount'):
            return make_response(jsonify(ERRORS['InvalidPaymentPost']), 404)

        if user.email == post_data.get('to'):
            return make_response(jsonify(ERRORS['InvalidEmailDestinatary']), 404)

        # Get destinatary from json and check if exists in DB.
        to = UserModel.query.filter_by(email=post_data.get('to')).first()
        if not to:
            return make_response(jsonify(ERRORS['InvalidEmailDestinatary']), 404)

        # Get amount to transfer from json and check if it is a valid amount.
        amount = post_data.get('amount')
        if amount > user.balance or not isinstance(amount, int) or amount <= 0:
            return make_response(jsonify(ERRORS['InvalidAmount']), 404)

        user.balance -= amount
        to.balance += amount

        db.session.add_all([user, to])
        db.session.commit()

        responseObject = {
            'status': 'success',
            'message': 'Payment has been sended.',
            'data': {
                'current_balance': user.balance
            }
        }
        return make_response(jsonify(responseObject), 200)

class Login(Resource):
    def post(self):
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = UserModel.query.filter_by(
                email=post_data.get('email')
              ).first()
            if user and UserModel.verify_password(
                user.password, post_data.get('password')
            ):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(responseObject), 200)
            else:
                return make_response(jsonify(ERRORS['InvalidEmailOrPassword']), 404)
        except Exception as e:
            return make_response(jsonify(ERRORS['Generic']), 500)

class Register(Resource):
    def post(self):
        # get the post data
        post_data = request.get_json()

        if not post_data.get('email'):
            return make_response(jsonify(ERRORS['InvalidEmailOrPassword']), 404)
        # check if user already exists
        user = UserModel.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                if not check_email(post_data.get('email')):
                    return make_response(jsonify(ERRORS['InvalidEmailFormat']), 422)

                user = UserModel(
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )
                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject), 201)
            except Exception as e:
                return make_response(jsonify(ERRORS['Generic']), 500)
        else:
            return make_response(jsonify(ERRORS['UserAlreadyExists']), 202)
