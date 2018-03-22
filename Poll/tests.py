from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()


class ListCreatePoll(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='neefemee@gmail.com', username='oluwanifemi')
        self.user.set_password('nifemi3')
        self.user.save()

        self.token = Token.objects.get(user=self.user).key

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.payload = {
            "title": "The next Ballon d\"or winner",
            "description": "We dont know yet",
            "starts": datetime.now(),
            "expires": datetime(2017, 4, 22, 14, 50),
            "options": [
                {"option": "Barrack Obama"},
                {"option": "Donald Trump"},
                {"option": "Damilola Adeyemi"}
            ]
        }
        self.url = reverse('list-create-poll')

    def test_can_create_poll_authenticated(self):
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
