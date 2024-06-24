from django.urls import reverse

from rest_framework import status

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from users.models import User


class UserTestCase(APITestCase):

    def setUp(self):
        pass
