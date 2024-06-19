from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_link


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.CharField(validators=[validate_link])

    class Meta:
        model = Lesson
        fields = ("id", "course", "title", "description", "video_link", "owner")


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons_list = LessonSerializer(source="lessons", many=True, read_only=True)

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
        )
