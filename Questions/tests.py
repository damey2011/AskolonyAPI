from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from Questions.models import Question, QuestionFollowing

User = get_user_model()


class QuestionCreateTestCases(TestCase):
    def setUp(self):
        self.q = Question.objects.create(title='This is a question ?', body='Body of the question')
        self.user = User.objects.create(email='neefemee@gmail.com', username='oluwanifemi')
        self.user.set_password('nifemi3')
        self.user.save()

        self.token = Token.objects.get(user=self.user).key

        self.client = APIClient()
        self.question_payload = {
            'title': 'What about the foundation?',
            'body': 'We bless the Almighty God for his faithfulness over our lives this time as always, and for his continuous agenda to transform us into his great vessels. We bless God for how he has helped us so far since we started and for manifesting himself greatly in our lives through all the successful programs we\'ve had. This season we’ve had a reason to travel to and fro the state for different programs and he has kept us safe, no accident, to him alone be all the praise. On the 4th of this month we had an axis program which gathered almost all the RCCF in the state together for the purpose of uniting us as one big family and to the glory of God, it was a huge success.' +
                    'Finally, we are trusting God to grant us more grace to achieve greater things in this little period that is remaining. But we are actually trusting God for a bus to help the fellowship in most of her activities as that’s one of our major challenges. We bless him also for his mercies towards us in this capacity and by his grace; we will be ready to do more if he commits more work into our hands.',
        }
        self.list_create_question = reverse('list-create-question')

    def test_can_create_question_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.list_create_question, self.question_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data['author'], 'Anonymous')

    def test_cannot_created_question_unauthenticated(self):
        client = APIClient()
        response = client.post(self.list_create_question, self.question_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_anonymous_question(self):
        question_payload = {
            'title': 'If the foundation be destroyed',
            'body': 'We bless the Almighty God for his faithfulness over our lives this time as always, and for his continuous agenda to transform us into his great vessels. We bless God for how he has helped us so far since we started and for manifesting himself greatly in our lives through all the successful programs we\'ve had. This season we’ve had a reason to travel to and fro the state for different programs and he has kept us safe, no accident, to him alone be all the praise. On the 4th of this month we had an axis program which gathered almost all the RCCF in the state together for the purpose of uniting us as one big family and to the glory of God, it was a huge success.' +
                    'Finally, we are trusting God to grant us more grace to achieve greater things in this little period that is remaining. But we are actually trusting God for a bus to help the fellowship in most of her activities as that’s one of our major challenges. We bless him also for his mercies towards us in this capacity and by his grace; we will be ready to do more if he commits more work into our hands.',
            'is_anonymous': True
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.list_create_question, question_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'], 'Anonymous')

    def test_can_edit_self_question(self):
        question_payload = {
            'title': 'The foundation will not be destroyed',
            'body': 'We bless the Almighty God for his faithfulness over our lives this time as always, and for his continuous agenda to transform us into his great vessels. We bless God for how he has helped us so far since we started and for manifesting himself greatly in our lives through all the successful programs we\'ve had. This season we’ve had a reason to travel to and fro the state for different programs and he has kept us safe, no accident, to him alone be all the praise. On the 4th of this month we had an axis program which gathered almost all the RCCF in the state together for the purpose of uniting us as one big family and to the glory of God, it was a huge success.' +
                    'Finally, we are trusting God to grant us more grace to achieve greater things in this little period that is remaining. But we are actually trusting God for a bus to help the fellowship in most of her activities as that’s one of our major challenges. We bless him also for his mercies towards us in this capacity and by his grace; we will be ready to do more if he commits more work into our hands.',
            'is_anonymous': True
        }

        q = Question.objects.create(title='Hello', body='bla bla bla', author=self.user)
        url = reverse('get-question', kwargs={'pk': q.pk})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.patch(url, question_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'The foundation will not be destroyed')

    def test_cannot_edit_other_user_question(self):
        user = User.objects.create(email='other@gmail.com', username='other')
        user.set_password('nifemi3')
        user.save()

        q = Question.objects.create(title='Hello', body='bla bla bla', author=user)
        url = reverse('get-question', kwargs={'pk': q.pk})

        question_payload = {
            'title': 'If the foundation be destroyed',
            'body': 'We bless the Almighty God for his faithfulness over our lives this time as always, and for his continuous agenda to transform us into his great vessels. We bless God for how he has helped us so far since we started and for manifesting himself greatly in our lives through all the successful programs we\'ve had. This season we’ve had a reason to travel to and fro the state for different programs and he has kept us safe, no accident, to him alone be all the praise. On the 4th of this month we had an axis program which gathered almost all the RCCF in the state together for the purpose of uniting us as one big family and to the glory of God, it was a huge success.' +
                    'Finally, we are trusting God to grant us more grace to achieve greater things in this little period that is remaining. But we are actually trusting God for a bus to help the fellowship in most of her activities as that’s one of our major challenges. We bless him also for his mercies towards us in this capacity and by his grace; we will be ready to do more if he commits more work into our hands.',
            'is_anonymous': True
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.patch(url, question_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class QuestionUpdateTestCases(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='neefemee@gmail.com', username='oluwanifemi')
        self.user.set_password('nifemi3')
        self.user.save()

        self.token = Token.objects.get(user=self.user).key

        self.client = APIClient()
        self.question_payload = {
            'title': 'If the foundation be destroyed',
            'body': 'We bless the Almighty God for his faithfulness over our lives this time as always, and for his continuous agenda to transform us into his great vessels. We bless God for how he has helped us so far since we started and for manifesting himself greatly in our lives through all the successful programs we\'ve had. This season we’ve had a reason to travel to and fro the state for different programs and he has kept us safe, no accident, to him alone be all the praise. On the 4th of this month we had an axis program which gathered almost all the RCCF in the state together for the purpose of uniting us as one big family and to the glory of God, it was a huge success.' +
                    'Finally, we are trusting God to grant us more grace to achieve greater things in this little period that is remaining. But we are actually trusting God for a bus to help the fellowship in most of her activities as that’s one of our major challenges. We bless him also for his mercies towards us in this capacity and by his grace; we will be ready to do more if he commits more work into our hands.',
        }

    def test_can_edit_self_question(self):
        question_payload = {
            'title': 'The foundation will not be destroyed',
            'body': 'We bless the Almighty God for his faithfulness over our lives this time as always, and for his continuous agenda to transform us into his great vessels. We bless God for how he has helped us so far since we started and for manifesting himself greatly in our lives through all the successful programs we\'ve had. This season we’ve had a reason to travel to and fro the state for different programs and he has kept us safe, no accident, to him alone be all the praise. On the 4th of this month we had an axis program which gathered almost all the RCCF in the state together for the purpose of uniting us as one big family and to the glory of God, it was a huge success.' +
                    'Finally, we are trusting God to grant us more grace to achieve greater things in this little period that is remaining. But we are actually trusting God for a bus to help the fellowship in most of her activities as that’s one of our major challenges. We bless him also for his mercies towards us in this capacity and by his grace; we will be ready to do more if he commits more work into our hands.',
            'is_anonymous': True
        }

        q = Question.objects.create(title='Hello', body='bla bla bla', author=self.user)
        url = reverse('get-question', kwargs={'pk': q.pk})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.patch(url, question_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'The foundation will not be destroyed')

    def test_cannot_edit_other_user_question(self):
        user = User.objects.create(email='other@gmail.com', username='other')
        user.set_password('nifemi3')
        user.save()

        q = Question.objects.create(title='Hello', body='bla bla bla', author=user)
        url = reverse('get-question', kwargs={'pk': q.pk})

        question_payload = {
            'title': 'If the foundation be destroyed',
            'body': 'We bless the Almighty God for his faithfulness over our lives this time as always, and for his continuous agenda to transform us into his great vessels. We bless God for how he has helped us so far since we started and for manifesting himself greatly in our lives through all the successful programs we\'ve had. This season we’ve had a reason to travel to and fro the state for different programs and he has kept us safe, no accident, to him alone be all the praise. On the 4th of this month we had an axis program which gathered almost all the RCCF in the state together for the purpose of uniting us as one big family and to the glory of God, it was a huge success.' +
                    'Finally, we are trusting God to grant us more grace to achieve greater things in this little period that is remaining. But we are actually trusting God for a bus to help the fellowship in most of her activities as that’s one of our major challenges. We bless him also for his mercies towards us in this capacity and by his grace; we will be ready to do more if he commits more work into our hands.',
            'is_anonymous': True
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.patch(url, question_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_edit_question_unauthenticated(self):
        question_payload = {
            'title': 'The foundation will not be destroyed',
            'body': 'We bless the Almighty God for his faithfulness over our lives this time as always, and for his continuous agenda to transform us into his great vessels. We bless God for how he has helped us so far since we started and for manifesting himself greatly in our lives through all the successful programs we\'ve had. This season we’ve had a reason to travel to and fro the state for different programs and he has kept us safe, no accident, to him alone be all the praise. On the 4th of this month we had an axis program which gathered almost all the RCCF in the state together for the purpose of uniting us as one big family and to the glory of God, it was a huge success.' +
                    'Finally, we are trusting God to grant us more grace to achieve greater things in this little period that is remaining. But we are actually trusting God for a bus to help the fellowship in most of her activities as that’s one of our major challenges. We bless him also for his mercies towards us in this capacity and by his grace; we will be ready to do more if he commits more work into our hands.',
            'is_anonymous': True
        }

        q = Question.objects.create(title='Hello', body='bla bla bla', author=self.user)
        url = reverse('get-question', kwargs={'pk': q.pk})
        client = APIClient()
        response = client.patch(url, question_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class QuestionFollowUnFollowTestCases(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='neefemee@gmail.com', username='oluwanifemi')
        self.user.set_password('nifemi3')
        self.user.save()

        self.client = APIClient()

        self.token = Token.objects.get(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.q = Question.objects.create(title='Hello', body='bla bla bla', author=self.user)

        self.follow_url = reverse('follow-question', kwargs={'pk': self.q.pk})
        self.unfollow_url = reverse('unfollow-question', kwargs={'pk': self.q.pk})

    def test_follow_question_authenticated(self):
        response = self.client.post(self.follow_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_question_post_unauthenticated(self):
        client = APIClient()
        response = client.post(self.follow_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unfollow_question_authenticated(self):
        QuestionFollowing.objects.create(user=self.user, question=self.q)
        response = self.client.post(self.unfollow_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_unfollow_question_unauthenticated(self):
        client = APIClient()
        QuestionFollowing.objects.create(user=self.user, question=self.q)
        response = client.delete(self.unfollow_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
