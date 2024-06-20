from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

from django_filters.rest_framework import DjangoFilterBackend

from users.models import User, Payments
from users.serializers import UserSerializer, PaymentSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """
    Эндпоинт для регистрации пользователя.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    # permission_classes = (AllowAny,) # использую для тестов

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


class UserUpdateAPIView(generics.UpdateAPIView):
    """
    Эндпоинт для обновления информации о пользователе.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()


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
