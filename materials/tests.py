from django.urls import reverse

from rest_framework import status

from rest_framework.response import Response

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@email.com", password="123")
        self.course = Course.objects.create(title="test_course")
        self.lesson = self.course.lessons.create(title="test_lesson", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson_detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        url = reverse("materials:lesson_create")

        data = {
            "title": "test_lesson_2",
            "course": self.course.pk,
            "video_link": "https://www.youtube.com/",
            "owner": self.user.pk}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)
        self.assertEqual(Lesson.objects.last().title, "test_lesson_2")
        self.assertEqual(Lesson.objects.last().owner, self.user)
        self.assertEqual(Lesson.objects.last().video_link, data['video_link'])

    def test_lesson_update(self):
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))

        data = {
            "title": "test_lesson_3",
        }

        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), "test_lesson_3")

    def test_lesson_delete(self):
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lesson_list")

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "course": self.course.pk,
                    "title": "test_lesson",
                    "description": None,
                    "video_link": None,
                    "owner": self.user.pk,
                }
            ]
        }

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.all().count(), 1)
        self.assertEqual(Lesson.objects.last().title, "test_lesson")
        self.assertEqual(Lesson.objects.last().owner, self.user)
        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@email.com", password="123")
        self.course = Course.objects.create(title="test_course")
        self.lesson = self.course.lessons.create(title="test_lesson", owner=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_subscription_create_or_delete(self):
        # url = reverse("/subscription/create/")

        data = {
            "user": self.user.pk,
            "course_id": self.course.pk,
        }

        response = self.client.post("/subscription/create/", data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        subs_item = Subscription.objects.filter(user=data['user'], course=data['course_id'])

        if subs_item.exists():
            subs_item.delete()
            self.assertEqual(subs_item.count(), 0)
            self.assertEqual(subs_item.exists(), False)
            print('тест на удаление подписки пройден')

        if not subs_item.exists():
            Subscription.objects.create(user=self.user, course=self.course)
            self.assertEqual(subs_item.exists(), True)
            self.assertEqual(subs_item.count(), 1)
            self.assertEqual(Subscription.objects.last().user, self.user)
            self.assertEqual(Subscription.objects.last().course_id, self.course.pk)
            print('тест на добавление подписки пройден')
