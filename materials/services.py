import requests

from drf_sample import settings
from rest_framework.exceptions import APIException


def convert_rub_to_usd(rub_price):
    usd_price = 0
    try:
        response = requests.get(
            f"{settings.CURRENCY_API_URL}v3/latest?apikey={settings.CURRENCY_API_KEY}&currencies=RUB"
        )
        response.raise_for_status()
        usd_rate = response.json()["data"]["RUB"]["value"]
        usd_price = rub_price / usd_rate
    except (requests.RequestException, ValueError) as e:
        raise APIException("Can't get currency rate") from e

    return usd_price
