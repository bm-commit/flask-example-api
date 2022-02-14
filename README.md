### Simple Flask API

Interview process challenge with Python. 

- Allow to Login and register users.
- Get current balance for user.
- Transactions between two users.

#### Endpoints

> _Version: /api/v1_

**GET /user/balance**

> Note: Token-Barer Authentication required.

**POST /user/payment/send**

Request:

```json
{
  "to": "test2@example.com",
  "amount": 10
}
```

> Note: Token-Barer Authentication required.

**POST /auth/login**

Request:

```json
{
  "email": "test@example.com",
  "password": "some_pass"
}
```

**POST /auth/register**

Request:

```json
{
  "email": "test@example.com",
  "password": "some_pass"
}
```
