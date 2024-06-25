from django.shortcuts import get_object_or_404

from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from materials.models import Course, Lesson, Subscription
from materials.paginations import CustomPagination
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    SubscriptionSerializer,
)
from materials.tasks import send_info_about_update
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """
    Эндпоинты для работы с курсами
    """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def get_permissions(self):
        """
        Метод получения разрешений
        :return: возвращает список разрешений
        """
        if self.action == "create":
            self.permission_classes = (
                IsAuthenticated,
                ~IsModer,
            )
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (
                IsAuthenticated,
                IsModer | IsOwner,
            )
        elif self.action == "destroy":
            self.permission_classes = (
                IsAuthenticated,
                ~IsModer | IsOwner,
            )
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Метод получения владельца курса
        :param serializer: на вход получаем сериализатор
        """
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        instance = serializer.save()
        queryset = Subscription.objects.filter(course=instance)

        owner = instance.owner.email
        subject = f"Обновление курса {instance.title}"
        message = f"Курс {instance.title} был обновлен, проверьте на сайте"

        for q in queryset:
            user = q.user.email

            if queryset.filter(user=q.user.pk).exists():
                send_info_about_update.delay(subject, message, user)
            else:
                print("Нет подписок на курс")
        return instance


def get_queryset(self, *args, **kwargs):
    """
    Метод получения курсов с фильтрацией по владельцу
    """
    queryset = super().get_queryset()
    queryset = queryset.filter(owner=self.request.user.pk)
    return queryset


# Lesson generics


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Эндпоинт создания урока
    """

    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        ~IsModer,
    )

    def perform_create(self, serializer):
        """
        Метод получения владельца урока
        :param serializer: на вход получаем сериализатор
        """
        lesson = serializer.save(owner=self.request.user)
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """
    Эндпоинт получения списка уроков
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self, *args, **kwargs):
        """
        Метод получения уроков с фильтрацией по владельцу
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user.pk)
        return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Эндпоинт получения детальной информации по уроку
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsModer | IsOwner,
    )


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Эндпоинт обновления информации по уроку
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsModer | IsOwner,
    )


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Эндпоинт удаления урока
    """

    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        ~IsModer | IsOwner,
    )


# Subscription ViewSet


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    Эндпоинты для работы с подписками
    """

    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def post(self, request, *args, **kwargs):
        """
        Метод создания подписки. Если подписка уже есть, то удаляет ее.
        :return: Возвращает сообщение об успешной подписке
        """
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            subs_item = Subscription(user=user, course=course_item)
            subs_item.save()
            message = "подписка добавлена"

        return Response(data={"message": message})
