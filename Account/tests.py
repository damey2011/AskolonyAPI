from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

# Create your tests here.
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from rest_framework.utils import json

from Account.models import UserFollowings
from Post.models import Post, PostFollow

User = get_user_model()


def get_token(username, password):
    data = {'username': 'oluwanifemi', 'password': 'nifemi3'}
    url = reverse('get_auth_token')
    client = APIClient()
    response = client.post(url, data, format='json')
    return response.data


class AccountCreateTestCases(TestCase):
    def setUp(self):
        self.user_payload = {'email': 'neefemee@gmail.com', 'password': 'nifemi3', 'username': 'oluwanifemi',
                             'first_name': 'First', 'last_name': 'Last'}
        self.url = reverse('sign-up')

    def test_create_account_with_correct_details(self):
        response = self.client.post(self.url, self.user_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_account_without_password(self):
        payload = {'email': 'neefemee@gmail.com', 'username': 'oluwanifemi',
                   'first_name': 'First', 'last_name': 'Last'}
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_account_with_short_password(self):
        payload = {'email': 'neefemee@gmail.com', 'password': 'nif', 'username': 'oluwanifemi',
                   'first_name': 'First', 'last_name': 'Last'}
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_account_with_duplicate_username(self):
        payload = {'email': 'neefemee@gmail.com', 'password': 'nifemi3', 'username': 'oluwanifemi',
                   'first_name': 'First', 'last_name': 'Last'}
        response = self.client.post(self.url, payload, format='json')
        payload = {'email': 'neefemee_diff@gmail.com', 'password': 'nifemi3', 'username': 'oluwanifemi',
                   'first_name': 'First', 'last_name': 'Last'}
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_account_with_duplicate_email(self):
        payload = {'email': 'neefemee@gmail.com', 'password': 'nifemi3', 'username': 'oluwanifemi',
                   'first_name': 'First', 'last_name': 'Last'}
        response = self.client.post(self.url, payload, format='json')

        payload = {'email': 'neefemee@gmail.com', 'password': 'nifemi3', 'username': 'oluwanifemi_diff',
                   'first_name': 'First', 'last_name': 'Last'}
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AccountRetrieveTestCases(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='oluwanifemi', email='neefemee@gmail.com')
        self.user.set_password = 'nifemi3'
        self.user.save()

        self.client = APIClient()
        self.token = Token.objects.get(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_can_get_valid_account(self):
        user = User.objects.filter().first()
        url = reverse('get-user', kwargs={'username': user.username})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_get_self_account(self):
        url = reverse('get-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('username'), 'oluwanifemi')

    def test_cannot_get_invalid_account(self):
        jargon = 'fdkofsngjnsjfn'
        url = reverse('get-user', kwargs={'username': jargon})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AccountUpdateTestCases(APITestCase):
    def setUp(self):
        self.username = 'oluwanifemi'
        self.user = User.objects.create(username=self.username, email='neefemee@gmail.com')
        self.user.set_password = 'nifemi3'
        self.user.save()

        self.client = APIClient()
        self.token = Token.objects.get(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_authenticated_update(self):
        url = reverse('get-user', kwargs={'username': self.user.username})
        data = {
            'bio': 'Hello there',
            'profile': {
                'college': 'Funaab',
                'works': 'Senseandserve',
                'lives': 'Ondo',
                'facebook_link': 'https://facebook.com/adeyemi',
                'twitter_link': 'https://twitter.com/nfiiz',
                'linked_in_profile': 'https://linkedin.com/profile/damey'
            }
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.patch(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('bio', None), 'Hello there')

    def test_unauthenticated_update(self):
        url = reverse('get-user', kwargs={'username': self.user.username})
        data = {
            'bio': 'Hello there',
            'profile': {
                'college': 'Funaab',
                'works': 'Senseandserve',
                'lives': 'Ondo',
                'facebook_link': 'https://facebook.com/adeyemi',
                'twitter_link': 'https://twitter.com/nfiiz',
                'linked_in_profile': 'https://linkedin.com/profile/damey'
            }
        }

        client = APIClient()
        response = client.patch(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_third_party_user_update(self):
        user = User.objects.create(username='testuser2', email='test@gmail.com')
        user.set_password('password')
        user.save()

        url = reverse('get-user', kwargs={'username': user.username})
        data = {
            'bio': 'Hello there',
            'profile': {
                'college': 'Funaab',
                'works': 'Senseandserve',
                'lives': 'Ondo',
                'facebook_link': 'https://facebook.com/adeyemi',
                'twitter_link': 'https://twitter.com/nfiiz',
                'linked_in_profile': 'https://linkedin.com/profile/damey'
            }
        }

        response = self.client.patch(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SignInTests(TestCase):
    def setUp(self):
        oluwanifemi = {'email': 'neefemee@gmail.com', 'password': 'nifemi3', 'username': 'oluwanifemi',
                       'first_name': 'First', 'last_name': 'Last'}
        damey2011 = {'email': 'adeyemi@gmail.com', 'password': 'nifemi3', 'username': 'damey2011',
                     'first_name': 'First', 'last_name': 'Last'}

        url = reverse('sign-up')
        self.user_response_1 = self.client.post(url, oluwanifemi, format='json')
        self.user_response_2 = self.client.post(url, damey2011, format='json')

    def test_correct_login_details(self):
        data = {'username': 'oluwanifemi', 'password': 'nifemi3'}
        url = reverse('get_auth_token')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data.get('token', None), None)

    def test_incorrect_login_details(self):
        data = {'username': 'oluwanifem', 'password': 'nifemi'}
        url = reverse('get_auth_token')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('token', None), None)


class AccountFollowTestCases(TestCase):
    def setUp(self):
        self.oluwanifemi = User.objects.create(username='oluwanifemi', email='neefemee@gmail.com')
        self.oluwanifemi.set_password = 'nifemi3'
        self.oluwanifemi.save()

        self.damey2011 = User.objects.create(username='damey2011', email='adeyemidamilola3@gmail.com')
        self.damey2011.set_password = 'nifemi3'
        self.damey2011.save()

        self.client = APIClient()

        self.follow_url = reverse('follow-user', kwargs={'username': self.damey2011.username})

        UserFollowings.objects.create(user=self.oluwanifemi, is_following=self.damey2011)

    """Test for oluwanifemi to follow damey2011"""

    def test_authenticated_follow(self):
        token = Token.objects.get(user=self.oluwanifemi).key
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.post(self.follow_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserFollowings.objects.all().count(), 1)

    def test_unauthenticated_follow(self):
        response = self.client.post(self.follow_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_self_follow(self):
        token = Token.objects.get(user=self.oluwanifemi).key
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.post(reverse('follow-user', kwargs={'username': self.oluwanifemi.username}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_followers(self):
        response = self.client.get(reverse('list-user-followers', kwargs={'username': self.damey2011.username}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)

    def test_retrieve_user_followings(self):
        response = self.client.get(reverse('list-user-followings', kwargs={'username': self.oluwanifemi.username}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)


class AccountUnFollowTestCases(TestCase):
    def setUp(self):
        self.oluwanifemi = User.objects.create(username='oluwanifemi', email='neefemee@gmail.com')
        self.oluwanifemi.set_password = 'nifemi3'
        self.oluwanifemi.save()

        self.damey2011 = User.objects.create(username='damey2011', email='adeyemidamilola3@gmail.com')
        self.damey2011.set_password = 'nifemi3'
        self.damey2011.save()

        self.user_following = UserFollowings.objects.create(user=self.oluwanifemi, is_following=self.damey2011)

        self.client = APIClient()

        self.unfollow_url = reverse('follow-user', kwargs={'username': self.damey2011.username})

    """Test for oluwanifemi to follow damey2011"""

    def test_authenticated_unfollow(self):
        token = Token.objects.get(user=self.oluwanifemi).key
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.delete(self.unfollow_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_unfollow(self):
        response = self.client.delete(self.unfollow_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RetrieveUsersFollowedPostTestCases(TestCase):
    def setUp(self):
        self.oluwanifemi = User.objects.create(username='oluwanifemi', email='neefemee@gmail.com')
        self.oluwanifemi.set_password = 'nifemi3'
        self.oluwanifemi.save()

        self.damey2011 = User.objects.create(username='damey2011', email='adeyemidamilola3@gmail.com')
        self.damey2011.set_password = 'nifemi3'
        self.damey2011.save()

        p = Post.objects.create(title='Hello', content='bla bla bla', user=self.oluwanifemi)
        p = Post.objects.create(title='Hello', content='bla bla bla', user=self.damey2011)

        PostFollow.objects.create(user=self.oluwanifemi, post=p)
        PostFollow.objects.create(user=self.damey2011, post=p)

        self.client = APIClient()
        token = Token.objects.get(user=self.oluwanifemi).key
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        self.get_oluwanifemi_posts_url = reverse('list-my-followed-posts')

    def test_oluwanifemi_can_retrieve_his_followed_posts(self):
        response = self.client.get(self.get_oluwanifemi_posts_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)


class RetrieveUserCreatedPostTestCases(TestCase):
    def setUp(self):
        self.oluwanifemi = User.objects.create(username='oluwanifemi', email='neefemee@gmail.com')
        self.oluwanifemi.set_password = 'nifemi3'
        self.oluwanifemi.save()

        self.damey2011 = User.objects.create(username='damey2011', email='adeyemidamilola3@gmail.com')
        self.damey2011.set_password = 'nifemi3'
        self.damey2011.save()

        Post.objects.create(title='Hello', content='bla bla bla', user=self.damey2011)
        Post.objects.create(title='Hello', content='bla bla bla', user=self.oluwanifemi)

        self.client = APIClient()
        token = Token.objects.get(user=self.oluwanifemi).key
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        self.get_oluwanifemi_posts_url = reverse('list-user-posts', kwargs={'username': self.oluwanifemi.username})

    def test_can_retrieve_oluwanifemi_posts(self):
        response = self.client.get(self.get_oluwanifemi_posts_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)

    def test_can_retrieve_oluwanifemi_polls(self):
        list_polls_url = reverse('list-my-polls')
        response = self.client.get(list_polls_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
