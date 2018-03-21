from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from Topic.models import Topic

User = get_user_model()


class TestGetDeleteAndCreateTopic(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='oluwanifemi', email='neefemee@gmail.com')
        self.topic = Topic.objects.create(name='Title of the next Topic', description='Hello description',
                                          created_by=self.user)

        self.client = APIClient()
        self.token = Token.objects.get(user=self.user).key

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.url = reverse('list-create-topic')
        self.payload = {
            'name': 'Coding',
            'description': ''
        }

    def test_can_create_topic_authenticated(self):
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_create_topic_unauthenticated(self):
        client = APIClient()
        response = client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_update_topic_authenticated(self):
        topic = Topic.objects.create(name='Title of the next Topic', description='Hello description',
                                     created_by=self.user)
        payload = {
            'name': 'Coding Updated',
            'description': 'Hello Desc'
        }
        url = reverse('get-topic', kwargs={'pk': topic.pk})
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), 'Coding Updated')

    def test_cannot_update_topic_unauthenticated(self):
        payload = {
            'name': 'Coding Updated',
            'description': 'Hello Desc'
        }
        url = reverse('get-topic', kwargs={'pk': self.topic.pk})
        client = APIClient()
        response = client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_topic(self):
        url = reverse('get-topic', kwargs={'pk': self.topic.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestFollowUnfollowTopic(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='oluwanifemi', email='neefemee@gmail.com')
        self.topic = Topic.objects.create(name='Title of the next Topic', description='Hello description',
                                          created_by=self.user)

        self.client = APIClient()
        self.token = Token.objects.get(user=self.user).key

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.url = reverse('follow-topic', kwargs={'pk': self.topic.pk})

    def test_follow_topic_authenticated(self):
        response = self.client.post(self.url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_follow_topic_unauthenticated(self):
        client = APIClient()
        response = client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unfollow_topic(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
