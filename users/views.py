import os

from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

import stripe

from django_filters.rest_framework import DjangoFilterBackend

from materials.models import Course
from users.models import User, Payments
from users.serializers import UserSerializer, PaymentSerializer, UserProfileSerializer

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


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

    def post(self, *args, **kwargs):
        super().post(*args, **kwargs)

        course_id = self.request.data.get("paid_course")
        course_item = get_object_or_404(Course, pk=course_id)

        payment_count = self.request.data.get("payment_count")

        stripe.Product.create(name=course_item.title)

        price = stripe.Price.create(
            unit_amount=payment_count * 100,
            currency="rub",
            product_data={"name": course_item.title},
        )

        session = stripe.checkout.Session.create(
            success_url="https://example.com/success",
            line_items=[{"price": price.id, "quantity": 1}],
            mode="payment",
        )

        return Response(data={"url": session.url})


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
