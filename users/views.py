import os

from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

import stripe

from django_filters.rest_framework import DjangoFilterBackend

from config.settings import STRIPE_SECRET_KEY
from materials.models import Course
from users.models import User, Payments
from users.serializers import UserSerializer, PaymentSerializer, UserProfileSerializer
from users.services import create_stripe_price, create_stripe_session

stripe.api_key = STRIPE_SECRET_KEY


class UserCreateAPIView(generics.CreateAPIView):
    """
    Эндпоинт для регистрации пользователя.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    """
    Эндпоинт для получения списка пользователей.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)  # использую для тестов


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """
    Эндпоинт для получения информации о пользователе.
    """

    serializer_class = UserSerializer

    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.user.pk == self.kwargs["pk"]:
            return UserSerializer
        else:
            return UserProfileSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    """
    Эндпоинт для обновления информации о пользователе.
    """

    serializer_class = UserSerializer

    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class UserDestroyAPIView(generics.DestroyAPIView):
    """
    Эндпоинт для удаления пользователя.
    """

    queryset = User.objects.all()


class PaymentCreateAPIView(generics.CreateAPIView):
    """
    Эндпоинт для создания платежа.
    """

    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        product_id = stripe.Product.create(name=f"Payment for {payment.paid_course.title or payment.paid_lesson.title}")

        price_id = create_stripe_price(product_id, payment.payment_count)

        session = create_stripe_session(price_id)

        # Обновление информации о платеже

        payment.payment_id = price_id
        payment.payment_link = session.url
        payment.tokens = session.id
        payment.save()

        return Response(data={"Ссылка на оплату": session.url})


class PaymentListAPIView(generics.ListAPIView):
    """
    Эндпоинт для получения списка платежей.
    """

    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = (
        "payment_method",
        "paid_course",
        "paid_lesson",
    )
    ordering_fields = ("data",)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """
    Эндпоинт для получения информации о платеже.
    """

    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()

    def get(self, *args, **kwargs):
        payment_data = super().get(*args, **kwargs).data
        payment = get_object_or_404(Payments, pk=self.kwargs["pk"])

        check_out = stripe.checkout.Session.retrieve(
            payment.tokens,
        )

        payment.status = check_out.payment_status
        payment.save()

        return Response(data={
            "Payment": payment_data,
            "Статус платежа": check_out.payment_status
        })


class PaymentUpdateAPIView(generics.UpdateAPIView):
    """
    Эндпоинт для обновления информации о платеже.
    """

    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()


class PaymentDestroyAPIView(generics.DestroyAPIView):
    """
    Эндпоинт для удаления платежа.
    """

    queryset = Payments.objects.all()
