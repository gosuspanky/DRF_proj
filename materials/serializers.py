from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()

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
        )


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            "course",
            "title",
            "description",
        )
