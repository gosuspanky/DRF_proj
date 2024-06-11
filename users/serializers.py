from rest_framework import serializers, filters

from users.models import User, Payments


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    filter_backends = [filters.OrderingFilter]
    filterset_fields = ('payment_method', 'paid_course', 'paid_lesson', )
    ordering_fields = ('data',)

    class Meta:
        model = Payments
        fields = ("id", 'data', 'payment_count', 'payment_method', 'paid_course', 'paid_lesson')
