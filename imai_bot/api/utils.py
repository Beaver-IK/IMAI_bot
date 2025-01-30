import requests
import json
from rest_framework.serializers import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

ENDPOINT = 'https://api.imeicheck.net/v1/checks'

def get_info(imei, token):
    """Функция запроса информации по Imay"""
    payload = json.dumps(dict(
        deviceId=imei,
        serviceId=12)
    )
    headers = {
    'Authorization': 'Bearer ' + token,
    'Accept-Language': 'ru',
    'Content-Type': 'application/json'
    }

    try:
        response = requests.request('POST',
                                ENDPOINT,
                                headers=headers,
                                data=payload)
    except Exception as e:
        return e
    
    data = json.loads(response.text)
    info = data.get('properties')
    if not info:
        return data
    return info

def already_use(data):
    """Функция проверки занятости username и telegram_id."""
    already_use = User.already_use(data)
    if already_use:
        raise ValidationError(already_use)
    return data