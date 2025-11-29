import requests

PAYIR_API_KEY = 'test'  # کلید تستی (سندباکس) - در حالت واقعی کلیدت رو از پنل Pay.ir بگیر
PAYIR_API_BASE = 'https://pay.ir/pg'


def send_payment_request(amount: int, callback_url: str):
    """
    ارسال درخواست پرداخت به درگاه Pay.ir
    """
    url = f"{PAYIR_API_BASE}/send"
    data = {
        'api': PAYIR_API_KEY,
        'amount': amount,
        'callback': callback_url,
        'description': 'تست پرداخت درگاه Pay.ir'
    }

    try:
        response = requests.post(url, data=data)
        result = response.json()
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

    if result.get('status') == 1:
        token = result.get('token')
        gateway_url = f"{PAYIR_API_BASE}/{token}"
        return {'status': 'ok', 'token': token, 'gateway_url': gateway_url}
    else:
        return {'status': 'error', 'message': result.get('errorMessage')}


def verify_payment(token: str):
    """
    بررسی وضعیت تراکنش پس از بازگشت از درگاه
    """
    url = f"{PAYIR_API_BASE}/verify"
    data = {
        'api': PAYIR_API_KEY,
        'token': token
    }

    try:
        response = requests.post(url, data=data)
        result = response.json()
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

    if result.get('status') == 1:
        return {
            'status': 'ok',
            'amount': result.get('amount'),
            'trans_id': result.get('transId')
        }
    else:
        return {
            'status': 'error',
            'message': result.get('errorMessage')
        }
