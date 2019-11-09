from flask import Blueprint
from flask_restful import Api
from .handlers import Balance, SendPayment, Login, Register
from .middlewares import check_token_based_authentication

user_bp = Blueprint('user', __name__)
api_user = Api(user_bp)

# MIDDLEWARE
@user_bp.before_request
def run_middleware():
    return check_token_based_authentication()

# USER ROUTES
api_user.add_resource(Balance, '/user/balance')
api_user.add_resource(SendPayment, '/user/payment/send')

# AUTHENTICATION ROUTES
auth_bp = Blueprint('auth', __name__)
api_auth = Api(auth_bp)

api_auth.add_resource(Login, '/auth/login')
api_auth.add_resource(Register, '/auth/register')
#Logout not implemented
