from django.urls import reverse, reverse_lazy
import requests

from drf_sample import settings
from rest_framework.exceptions import APIException

import stripe


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


class StripeAPI:
    def __init__(self):
        self.stripe = stripe
        self.stripe.api_key = settings.STRIPE_API_KEY

    def get_products(self):
        return self.stripe.Product.list()

    def create_product(self, name, price):
        product = self.stripe.Product.create(name=name)
        return self.stripe.Price.create(
            product=product.id,
            unit_amount=int(price * 100),
            currency="usd",
        )

    def create_session(self, price_id, base_url, course_id):
        return self.stripe.checkout.Session.create(
            line_items=[{"price": price_id, "quantity": 1}],
            mode="payment",
            success_url=base_url + reverse("materials:success", args=[course_id]),
            cancel_url=base_url + reverse("materials:cancel"),
        )
