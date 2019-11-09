ERRORS = {
    "MalformeBearerToken": {
        'status': 'fail',
        'message': 'Bearer token malformed.'
    },
    "InvalidToken":{
        'status': 'fail',
        'message': 'Provide a valid auth token.'
    },
    "InvalidEmailDestinatary":{
        'status': 'fail',
        'message': 'Invalid email destinatary.'
    },
    "InvalidEmailFormat":{
        'status': 'fail',
        'message': 'Invalid email format.'
    },
    "InvalidAmount":{
        'status': 'fail',
        'message': 'Invalid amount.'
    },
    "InvalidEmailOrPassword":{
        'status': 'fail',
        'message': 'Invalid email or password.'
    },
    "Generic":{
        'status': 'fail',
        'message': 'Something went wrong, try again leter.'
    },
    "UserAlreadyExists":{
        'status': 'fail',
        'message': 'User already exists. Please Log in.'
    },
    "InvalidPaymentPost":{
        'status': 'fail',
        'message': 'Please fulfill valid values in the request.'
    }
}

def get_custom_error(error):
    return {
        'status': 'fail',
        'message': error
    }
