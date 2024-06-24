from rest_framework import serializers

from users.models import User, Payments


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор платежей пользователя.
    """

    class Meta:
        model = Payments
        exclude = (
            "tokens",
            "payment_id",
        )


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователей.
    """

    payments_history = PaymentSerializer(many=True, source="payment", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone_number",
            "city",
            "first_name",
            "last_name",
            "is_active",
            "payments_history",
        )


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователей.
    """

    class Meta:
        model = User
        exclude = (
            "password",
            "last_name",
        )
