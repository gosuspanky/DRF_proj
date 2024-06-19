from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_link


# class SubscriptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Subscription
#         fields = ("id", "user", "course", "date")


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.CharField(validators=[validate_link])

    class Meta:
        model = Lesson
        fields = ("id", "course", "title", "description", "video_link", "owner")


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    lessons_list = LessonSerializer(source="lessons", many=True, read_only=True)

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user=self.context["request"].user, course=obj
        ).exists()

    @staticmethod
    def get_lessons_count(obj):
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "lessons_count",
            "owner",
            "lessons_list",
            "is_subscribed",
        )
