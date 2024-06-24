from django.urls import reverse

from rest_framework import status

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

        url_2 = reverse("materials:lesson_detail", args=(65,))
        response_2 = self.client.get(url_2)
        self.assertEqual(response_2.status_code, status.HTTP_404_NOT_FOUND)

    def test_lesson_create(self):
        url = reverse("materials:lesson_create")

        data = {
            "title": "test_lesson_2",
            "course": self.course.pk,
            "video_link": "https://www.youtube.com/",
            "owner": self.user.pk,
        }

        data_2 = {
            "title": "test_lesson_3",
            "course": self.course.pk,
            "video_link": "https://www.vk.ru/",
            "owner": self.user.pk,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)
        self.assertEqual(Lesson.objects.last().title, "test_lesson_2")
        self.assertEqual(Lesson.objects.last().owner, self.user)
        self.assertEqual(Lesson.objects.last().video_link, data["video_link"])

        response = self.client.post(url, data_2)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_lesson_update(self):
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))

        data = {
            "title": "test_lesson_3",
        }

        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "test_lesson_3")

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
            ],
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

        data = {
            "user": self.user.pk,
            "course_id": self.course.pk,
        }

        response = self.client.post("/subscription/create/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        subs_item = Subscription.objects.filter(
            user=data["user"], course=data["course_id"]
        )

        if subs_item.exists():
            subs_item.delete()
            self.assertEqual(subs_item.count(), 0)
            self.assertEqual(subs_item.exists(), False)
            print("тест на удаление подписки пройден")

        if not subs_item.exists():
            Subscription.objects.create(user=self.user, course=self.course)
            self.assertEqual(subs_item.exists(), True)
            self.assertEqual(subs_item.count(), 1)
            self.assertEqual(Subscription.objects.last().user, self.user)
            self.assertEqual(Subscription.objects.last().course_id, self.course.pk)
            print("тест на добавление подписки пройден")

        self.client = APIClient()

        if not self.user.is_authenticated:
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@email.com", password="123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="test_course", owner=self.user)

    def test_course_retrieve(self):
        response = self.client.get(f"/materials/{self.course.pk}/")
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(data.get("title"), self.course.title)

        response_2 = self.client.get(f"/materials/65/")

        self.assertEqual(response_2.status_code, status.HTTP_404_NOT_FOUND)

    def test_course_create(self):
        data = {"title": "test_course_2", "description": "test_course_description"}
        response = self.client.post("/materials/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Course.objects.all().count(), 2)
        self.assertEqual(Course.objects.last().title, "test_course_2")
        self.assertEqual(Course.objects.last().owner, self.user)

    def test_course_update(self):
        data = {
            "title": "test_course_3",
        }

        response = self.client.patch(f"/materials/{self.course.pk}/", data)
        data = response.json()
        print(data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "test_course_3")

    def test_course_delete(self):
        response = self.client.delete(f"/materials/{self.course.pk}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        response = self.client.get(f"/materials/")

        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "title": "test_course",
                    "description": None,
                    "lessons_count": 0,
                    "owner": self.user.pk,
                    "lessons_list": [],
                    "is_subscribed": False,
                }
            ],
        }

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.all().count(), 1)
        self.assertEqual(Course.objects.last().title, "test_course")
        self.assertEqual(Course.objects.last().owner, self.user)
        self.assertEqual(data, result)
