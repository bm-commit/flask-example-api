import unittest
import json

from run import create_app
from users.model import db, User as UserModel


app = create_app('testing')
ctx = app.app_context()

class TestUserModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ctx.push()
        db.create_all()
        print('**** START TestUserModel ****')

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        ctx.pop()
        print('\n**** END TestUserModel ****')

    def test_encode_auth_token(self):
        user = UserModel(
            email='test@example.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = UserModel(
            email='test@test.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(UserModel.decode_auth_token(auth_token) == 1)


class TestUserRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ctx.push()
        db.create_all()
        print('**** START TestUserRoutes ****')

    def setUp(self):
        self.client = app.test_client()
        self.api_version = "api/v1"

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        ctx.pop()
        print('\n**** END TestUserRoutes ****')


    def test_registration(self):
        """ Test for user registration """
        with self.client:
            response = self.client.post(
                self.api_version + '/auth/register',
                data=json.dumps(dict(
                    email='user@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully registered.')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email"""
        user = UserModel(
            email='user1@gmail.com',
            password='test'
        )
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.post(
                self.api_version + '/auth/register',
                data=json.dumps(dict(
                    email='user1@gmail.com',
                    password='test'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'User already exists. Please Log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)

    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            # user registration
            resp_register = self.client.post(
                self.api_version + '/auth/register',
                data=json.dumps(dict(
                    email='myaccount@gmail.com',
                    password='123456'
                )),
                content_type='application/json',
            )
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.'
            )
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # registered user login
            response = self.client.post(
                self.api_version + '/auth/login',
                data=json.dumps(dict(
                    email='myaccount@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            response = self.client.post(
                self.api_version + '/auth/login',
                data=json.dumps(dict(
                    email='account@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid email or password.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_user_balance(self):
        """ Test for user status """
        with self.client:
            resp_register = self.client.post(
                self.api_version + '/auth/register',
                data=json.dumps(dict(
                    email='my_test_user@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            response = self.client.get(
                self.api_version + '/user/balance',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['email'] == 'my_test_user@gmail.com')
            self.assertTrue(data['data']['current_balance'] == 100)
            self.assertEqual(response.status_code, 200)

    def test_user_payment(self):
        """ Test for user status """
        with self.client:
            resp_register = self.client.post(
                self.api_version + '/auth/register',
                data=json.dumps(dict(
                    email='alice@gmail.com',
                    password='alice_account'
                )),
                content_type='application/json'
            )
            resp_register_two = self.client.post(
                self.api_version + '/auth/register',
                data=json.dumps(dict(
                    email='bob@gmail.com',
                    password='bob_account'
                )),
                content_type='application/json'
            )
            # Transfer money from Alice to Bob -> 50
            resp_transfer = self.client.post(
                self.api_version + '/user/payment/send',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                ),
                data=json.dumps(dict(
                    to='bob@gmail.com',
                    amount=50
                )),
                content_type='application/json'
            )

            data = json.loads(resp_transfer.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Payment has been sended.')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['current_balance'] == 50)
            self.assertEqual(resp_transfer.status_code, 200)

    def test_user_payment_invalid_amount(self):
        """ Test for user status """
        with self.client:
            user_response = self.client.post(
                self.api_version + '/auth/login',
                data=json.dumps(dict(
                    email='alice@gmail.com',
                    password='alice_account'
                )),
                content_type='application/json'
            )
            # Transfer money from Alice to Bob -> 50
            resp_transfer = self.client.post(
                self.api_version + '/user/payment/send',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        user_response.data.decode()
                    )['auth_token']
                ),
                data=json.dumps(dict(
                    to='bob@gmail.com',
                    amount=150
                )),
                content_type='application/json'
            )

            data = json.loads(resp_transfer.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid amount.')
            self.assertEqual(resp_transfer.status_code, 404)

    def test_user_payment_invalid_receiver(self):
        """ Test for user status """
        with self.client:
            user_response = self.client.post(
                self.api_version + '/auth/login',
                data=json.dumps(dict(
                    email='alice@gmail.com',
                    password='alice_account'
                )),
                content_type='application/json'
            )
            # Transfer money from Alice to Bob -> 50
            resp_transfer = self.client.post(
                self.api_version + '/user/payment/send',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        user_response.data.decode()
                    )['auth_token']
                ),
                data=json.dumps(dict(
                    to='bob_1@gmail.com',
                    amount=50
                )),
                content_type='application/json'
            )

            data = json.loads(resp_transfer.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid email destinatary.')
            self.assertEqual(resp_transfer.status_code, 404)


if __name__ == '__main__':
    unittest.main()
