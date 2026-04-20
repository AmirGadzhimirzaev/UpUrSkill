import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def stripe_product_create(product_name):
    """Создает продукт в страйп"""
    return stripe.Product.create(name=product_name)


def stripe_create_prise(product_id, amount):
    """Создает цену в страйп"""
    return stripe.Price.create(
        product=product_id,
        currency="usd",
        unit_amount=amount * 100
    )


def stripe_create_session(price_id):
    """Создает сессию в страйп"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url, session.payment_status, session.currency
