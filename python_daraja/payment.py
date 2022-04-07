import datetime

import requests
import base64

CONSUMER_KEY: str = ""
CONSUMER_SECRET: str = ""
PASSKEY: str = ""
SHORT_CODE: str = ""
ACCOUNT_TYPE: str = ""


def _get_trans_type():
    if ACCOUNT_TYPE == "PAYBILL":
        trans_type = "CustomerPayBillOnline"
    else:
        trans_type = "CustomerBuyGoodsOnline"
    return trans_type


def _get_password():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    data_to_encode = SHORT_CODE + PASSKEY + timestamp

    online_password = base64.b64encode(data_to_encode.encode('ascii'))
    decode_password = online_password.decode('utf-8')
    return decode_password


def _get_access_token() -> str:
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    encoded_creds = f"{CONSUMER_KEY}:{CONSUMER_SECRET}".encode('ascii')
    b64_creds = base64.b64encode(encoded_creds)

    payload = {}
    headers = {
        'Authorization': f"Basic {b64_creds.decode('utf-8')}"
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return dict(response.json())["access_token"]


def trigger_stk_push(phone_number: int, amount: int, callback_url: str, account_ref: str, description: str) -> dict:
    """

    :param phone_number: Customer Phone Number
    :param amount: Amount to be paid
    :param callback_url: Your callback URL configured in the dashboard
    :param account_ref: Account Reference (e.g. Company Name/Business Name)
    :param description: Transaction Description
    :return: Python Dictionary with transaction info
    """

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {_get_access_token()}'
    }

    payload = {
        "BusinessShortCode": int(SHORT_CODE),
        "Password": _get_password(),
        "Timestamp": int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')),
        "TransactionType": _get_trans_type(),
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": int(SHORT_CODE),
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": account_ref,
        "TransactionDesc": description
    }

    response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
                                headers=headers, data=payload)
    return dict(response.json())


def query_stk_push(checkout_request_id: str) -> dict:
    """

    :param checkout_request_id: Acquired from the result of successful STK push payment
    :return: Python Dictionary with transaction info
    """

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {_get_access_token()}'
    }
    payload = {
        "BusinessShortCode": int(SHORT_CODE),
        "Password": _get_password(),
        "Timestamp": int(datetime.datetime.now().strftime('%Y%m%d%H%M%S')),
        "CheckoutRequestID": checkout_request_id,
    }
    response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query', headers=headers,
                                data=payload)
    return dict(response.json())


# TODO: To be revisited
def register_urls(confirmation_url: str, validation_url: str, response_type: str):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {_get_access_token()}'
    }

    payload = {
        "ShortCode": SHORT_CODE,
        "ResponseType": response_type,
        "ConfirmationURL": confirmation_url,
        "ValidationURL": validation_url,
    }

    response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl', headers=headers,
                                data=payload)
    return dict(response.json())


# TODO: To be revisited
def c2b_transaction(amount: int, customer_phone_number: str):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {_get_access_token()}'
    }
    payload = {
        "ShortCode": int(SHORT_CODE),
        "CommandID": _get_trans_type(),
        "amount": amount,
        "MSISDN": customer_phone_number,
        "BillRefNumber": "examplepayment",
    }
    if _get_trans_type() == 'CustomerBuyGoodsOnline':
        payload["BillRefNumber"] = ""

    response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate', headers=headers,
                                data=payload)
    return dict(response.json())
