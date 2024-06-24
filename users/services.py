import stripe

from config.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


class CreateStripePayment:
    """
    Класс для создания продукта, цены и сессии для оплаты.
    """

    def __init__(self, course_title, payment_count):
        self.course_title = course_title
        self.payment_count = payment_count

        # self.stripe_product = None
        # self.price = None
        # self.session = None

    def create_stripe_product(self):
        """
        Создание продукта для курса.
        """
        stripe_product = stripe.Product.create(name=self.course_title)
        return stripe_product

    def create_stripe_price(self):
        """
        Создание цены для курса.
        """
        price = stripe.Price.create(
            unit_amount=int(self.payment_count * 100),
            currency="rub",
            product={"name": self.course_title},
        )
        return price

    def create_stripe_session(self):
        """
        Создание сессии для оплаты.
        """
        price = self.create_stripe_price()

        session = stripe.checkout.Session.create(
            success_url="https://example.com/success",
            line_items=[{"price": price.id, "quantity": 1}],
            mode="payment",
        )
        return session

    def get_session_url(self):
        session = self.create_stripe_session()
        return session.url

    def create_stripe_checkout(self):
        """
        Получение проверки.
        """
        session = self.create_stripe_session()
        check_out = stripe.checkout.Session.retrieve(
            session.id,
        )
        return check_out
