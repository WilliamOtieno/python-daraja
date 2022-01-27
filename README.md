# Python Daraja

### Description

Python Wrapper for handling payment requests through the Daraja MPESA API

### Contribution

- Refer to the [CONTRIBUTING GUIDE](/CONTRIBUTING.md).

## Usage

### Installation
```sh
pip install python-daraja
```

### Initial Setup

- Set the following constants first before proceeding

```python
from python_daraja import payment


payment.SHORT_CODE = "YOUR_SHORTCODE"
payment.PASSKEY = "YOUR PASSKEY"
payment.CONSUMER_SECRET = "YOUR CONSUMER SECRET"
payment.CONSUMER_KEY = "YOUR CONSUMER KEY"
payment.ACCOUNT_TYPE = "PAYBILL"  # Set to TILL to use BuyGoods instead of Pay Bill
```

- The first function to call is one which would trigger an automatic STK Push on your customer's phone. There is no
  simpler way of knowing whether the customer has successfully paid or not (failures such as inputting the wrong PIN or
  just cancelling the request altogether). You are therefore advised to set up a simple server with an endpoint that
  will accept `POST` requests from Daraja API with the details of the transaction.
- For the server, it must be secure (`https` instead of `http`), it must not be `localhost` nor `127.0.0.1:$PORT`.
- You can use services like `ngrok` to tunnel `localhost` to live secure server.
- Your server's endpoint should also accept a `POST`  request hence you may need to disable constraints such as `CSRF`
  (outside the scope of this project).
- If at all you must have CSRF Protection in your server, then you need to allow requests originating from the following
  IP addresses (whitelisting):
    - 192.201.214.200
    - 196.201.214.206
    - 196.201.213.114
    - 196.201.214.207
    - 196.201.214.208
    - 196.201.213.44
    - 196.201.212.127
    - 196.201.212.128
    - 196.201.212.129
    - 196.201.212.136
    - 196.201.212.74
    - 196.201.212.69
- You can now proceed by triggering the payment process; you should expect a Python Dict object with the results of the
  process. This will only tell you whether it was successful and not whether the customer has actually paid.

```python
from python_daraja import payment


details = payment.trigger_stk_push(phone_number=2547123456, amount=1, callback_url='https://your-domain/callback/',
                                   description='Payment for services rendered',
                                   account_ref='Python Good PHP Bad and Co.')
print(details)
```
- The MPESA Gateway will then send some `POST` data to your endpoint if the customer pays, otherwise, you will not
receive any data showing that your customer hasn't paid a dime.


- It is advisable to save the details received from the previous method call to a DB of your choice. Some of those
details are used for other subsequent method calls especially in getting the transaction status of your payment requests.
- In order to query the details of a payment request made through the automatic STK Push above:-
```python
from python_daraja import payment


details = payment.query_stk_push(checkout_request_id='ws_CO_DMZ_123212312_2342347678234')
print(details)
```
- Getting a `0` as the Response Code or Result Code generally means that the transaction was successful, any other digit
signifies otherwise.


### Remarks
 - Unfortunately as of the moment of release of this package, Safaricom has internal problems with other types of 
transactions such as `C2B`. Maintainers of the project will work on implementing more features when the issues are addressed.



[![Sponsor Python Daraja](https://cdn.buymeacoffee.com/buttons/default-red.png)](https://dashboard.flutterwave.com/donate/34m2kdigwskp)

