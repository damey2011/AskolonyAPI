from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from Post.models import Post, PostFollow, Comment

User = get_user_model()


class PostCreateTestCases(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='neefemee@gmail.com', username='oluwanifemi')
        self.user.set_password('nifemi3')
        self.user.save()

        self.token = Token.objects.get(user=self.user).key

        self.client = APIClient()
        self.post_payload = {
            'title': 'If the foundation be destroyed',
            'content': 'We bless the Almighty God for his faithfulness over our lives this time as always, and for his continuous agenda to transform us into his great vessels. We bless God for how he has helped us so far since we started and for manifesting himself greatly in our lives through all the successful programs we\'ve had. This season we’ve had a reason to travel to and fro the state for different programs and he has kept us safe, no accident, to him alone be all the praise. On the 4th of this month we had an axis program which gathered almost all the RCCF in the state together for the purpose of uniting us as one big family and to the glory of God, it was a huge success.' +
                       'Finally, we are trusting God to grant us more grace to achieve greater things in this little period that is remaining. But we are actually trusting God for a bus to help the fellowship in most of her activities as that’s one of our major challenges. We bless him also for his mercies towards us in this capacity and by his grace; we will be ready to do more if he commits more work into our hands.',
        }
        self.create_post_url = reverse('create-post')

    def test_can_create_post_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.create_post_url, self.post_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data['user'], 'Anonymous')

    def test_cannot_created_post_unauthenticated(self):
        client = APIClient()
        response = client.post(self.create_post_url, self.post_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_anonymous_post(self):
        post_payload = {
            'title': 'If the foundation be destroyed',
            'content': 'We bless the Almighty God for his faithfulness over our lives this time as always, and for his continuous agenda to transform us into his great vessels. We bless God for how he has helped us so far since we started and for manifesting himself greatly in our lives through all the successful programs we\'ve had. This season we’ve had a reason to travel to and fro the state for different programs and he has kept us safe, no accident, to him alone be all the praise. On the 4th of this month we had an axis program which gathered almost all the RCCF in the state together for the purpose of uniting us as one big family and to the glory of God, it was a huge success.' +
                       'Finally, we are trusting God to grant us more grace to achieve greater things in this little period that is remaining. But we are actually trusting God for a bus to help the fellowship in most of her activities as that’s one of our major challenges. We bless him also for his mercies towards us in this capacity and by his grace; we will be ready to do more if he commits more work into our hands.',
            'is_anonymous': True
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.create_post_url, post_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], 'Anonymous')

    def test_can_edit_self_post(self):
        post_payload = {
            'title': 'The foundation will not be destroyed',
            'content': 'We bless the Almighty God for his faithfulness over our lives this time as always, and for his continuous agenda to transform us into his great vessels. We bless God for how he has helped us so far since we started and for manifesting himself greatly in our lives through all the successful programs we\'ve had. This season we’ve had a reason to travel to and fro the state for different programs and he has kept us safe, no accident, to him alone be all the praise. On the 4th of this month we had an axis program which gathered almost all the RCCF in the state together for the purpose of uniting us as one big family and to the glory of God, it was a huge success.' +
                       'Finally, we are trusting God to grant us more grace to achieve greater things in this little period that is remaining. But we are actually trusting God for a bus to help the fellowship in most of her activities as that’s one of our major challenges. We bless him also for his mercies towards us in this capacity and by his grace; we will be ready to do more if he commits more work into our hands.',
            'is_anonymous': True
        }

        p = Post.objects.create(title='Hello', content='bla bla bla', user=self.user)
        url = reverse('get-post', kwargs={'pk': p.pk})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.patch(url, post_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'The foundation will not be destroyed')

    def test_cannot_edit_other_user_post(self):
        user = User.objects.create(email='other@gmail.com', username='other')
        user.set_password('nifemi3')
        user.save()

        p = Post.objects.create(title='Hello', content='bla bla bla', user=user)
        url = reverse('get-post', kwargs={'pk': p.pk})

        post_payload = {
            'title': 'If the foundation be destroyed',
            'content': 'We bless the Almighty God for his faithfulness over our lives this time as always, and for his continuous agenda to transform us into his great vessels. We bless God for how he has helped us so far since we started and for manifesting himself greatly in our lives through all the successful programs we\'ve had. This season we’ve had a reason to travel to and fro the state for different programs and he has kept us safe, no accident, to him alone be all the praise. On the 4th of this month we had an axis program which gathered almost all the RCCF in the state together for the purpose of uniting us as one big family and to the glory of God, it was a huge success.' +
                       'Finally, we are trusting God to grant us more grace to achieve greater things in this little period that is remaining. But we are actually trusting God for a bus to help the fellowship in most of her activities as that’s one of our major challenges. We bless him also for his mercies towards us in this capacity and by his grace; we will be ready to do more if he commits more work into our hands.',
            'is_anonymous': True
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.patch(url, post_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostUpdateTestCases(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='neefemee@gmail.com', username='oluwanifemi')
        self.user.set_password('nifemi3')
        self.user.save()

        self.token = Token.objects.get(user=self.user).key

        self.client = APIClient()
        self.post_payload = {
            'title': 'If the foundation be destroyed',
            'content': 'We bless the Almighty God for his faithfulness over our lives this time as always, and for his continuous agenda to transform us into his great vessels. We bless God for how he has helped us so far since we started and for manifesting himself greatly in our lives through all the successful programs we\'ve had. This season we’ve had a reason to travel to and fro the state for different programs and he has kept us safe, no accident, to him alone be all the praise. On the 4th of this month we had an axis program which gathered almost all the RCCF in the state together for the purpose of uniting us as one big family and to the glory of God, it was a huge success.' +
                       'Finally, we are trusting God to grant us more grace to achieve greater things in this little period that is remaining. But we are actually trusting God for a bus to help the fellowship in most of her activities as that’s one of our major challenges. We bless him also for his mercies towards us in this capacity and by his grace; we will be ready to do more if he commits more work into our hands.',
        }

    def test_can_edit_self_post(self):
        post_payload = {
            'title': 'The foundation will not be destroyed',
            'content': 'We bless the Almighty God for his faithfulness over our lives this time as always, and for his continuous agenda to transform us into his great vessels. We bless God for how he has helped us so far since we started and for manifesting himself greatly in our lives through all the successful programs we\'ve had. This season we’ve had a reason to travel to and fro the state for different programs and he has kept us safe, no accident, to him alone be all the praise. On the 4th of this month we had an axis program which gathered almost all the RCCF in the state together for the purpose of uniting us as one big family and to the glory of God, it was a huge success.' +
                       'Finally, we are trusting God to grant us more grace to achieve greater things in this little period that is remaining. But we are actually trusting God for a bus to help the fellowship in most of her activities as that’s one of our major challenges. We bless him also for his mercies towards us in this capacity and by his grace; we will be ready to do more if he commits more work into our hands.',
            'is_anonymous': True
        }

        p = Post.objects.create(title='Hello', content='bla bla bla', user=self.user)
        url = reverse('get-post', kwargs={'pk': p.pk})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.patch(url, post_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'The foundation will not be destroyed')

    def test_cannot_edit_other_user_post(self):
        user = User.objects.create(email='other@gmail.com', username='other')
        user.set_password('nifemi3')
        user.save()

        p = Post.objects.create(title='Hello', content='bla bla bla', user=user)
        url = reverse('get-post', kwargs={'pk': p.pk})

        post_payload = {
            'title': 'If the foundation be destroyed',
            'content': 'We bless the Almighty God for his faithfulness over our lives this time as always, and for his continuous agenda to transform us into his great vessels. We bless God for how he has helped us so far since we started and for manifesting himself greatly in our lives through all the successful programs we\'ve had. This season we’ve had a reason to travel to and fro the state for different programs and he has kept us safe, no accident, to him alone be all the praise. On the 4th of this month we had an axis program which gathered almost all the RCCF in the state together for the purpose of uniting us as one big family and to the glory of God, it was a huge success.' +
                       'Finally, we are trusting God to grant us more grace to achieve greater things in this little period that is remaining. But we are actually trusting God for a bus to help the fellowship in most of her activities as that’s one of our major challenges. We bless him also for his mercies towards us in this capacity and by his grace; we will be ready to do more if he commits more work into our hands.',
            'is_anonymous': True
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.patch(url, post_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_edit_post_unauthenticated(self):
        post_payload = {
            'title': 'The foundation will not be destroyed',
            'content': 'We bless the Almighty God for his faithfulness over our lives this time as always, and for his continuous agenda to transform us into his great vessels. We bless God for how he has helped us so far since we started and for manifesting himself greatly in our lives through all the successful programs we\'ve had. This season we’ve had a reason to travel to and fro the state for different programs and he has kept us safe, no accident, to him alone be all the praise. On the 4th of this month we had an axis program which gathered almost all the RCCF in the state together for the purpose of uniting us as one big family and to the glory of God, it was a huge success.' +
                       'Finally, we are trusting God to grant us more grace to achieve greater things in this little period that is remaining. But we are actually trusting God for a bus to help the fellowship in most of her activities as that’s one of our major challenges. We bless him also for his mercies towards us in this capacity and by his grace; we will be ready to do more if he commits more work into our hands.',
            'is_anonymous': True
        }

        p = Post.objects.create(title='Hello', content='bla bla bla', user=self.user)
        url = reverse('get-post', kwargs={'pk': p.pk})
        client = APIClient()
        response = client.patch(url, post_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PostFollowUnfollowTestCases(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='neefemee@gmail.com', username='oluwanifemi')
        self.user.set_password('nifemi3')
        self.user.save()

        token = Token.objects.get(user=self.user).key

        self.client = APIClient()
        self.post_payload = {
            'title': 'If the foundation be destroyed',
            'content': 'We bless the Almighty God for his faithfulness over our lives this time as always, and for his continuous agenda to transform us into his great vessels. We bless God for how he has helped us so far since we started and for manifesting himself greatly in our lives through all the successful programs we\'ve had. This season we’ve had a reason to travel to and fro the state for different programs and he has kept us safe, no accident, to him alone be all the praise. On the 4th of this month we had an axis program which gathered almost all the RCCF in the state together for the purpose of uniting us as one big family and to the glory of God, it was a huge success.' +
                       'Finally, we are trusting God to grant us more grace to achieve greater things in this little period that is remaining. But we are actually trusting God for a bus to help the fellowship in most of her activities as that’s one of our major challenges. We bless him also for his mercies towards us in this capacity and by his grace; we will be ready to do more if he commits more work into our hands.',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.p = Post.objects.create(title='Hello', content='Content Welcome', user=self.user)

        self.follow_post_url = reverse('follow-post', kwargs={'pk': self.p.pk})

    def test_follow_post_authenticated(self):
        response = self.client.post(self.follow_post_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_follow_post_unauthenticated(self):
        client = APIClient()
        response = client.post(self.follow_post_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unfollow_post_authenticated(self):
        PostFollow.objects.create(user=self.user, post=self.p)
        response = self.client.delete(self.follow_post_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_unfollow_post_unauthenticated(self):
        client = APIClient()
        PostFollow.objects.create(user=self.user, post=self.p)
        response = client.delete(self.follow_post_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CommentCreateTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='neefemee@gmail.com', username='oluwanifemi')
        self.user.set_password('nifemi3')
        self.user.save()

        self.token = Token.objects.get(user=self.user).key
        self.p = Post.objects.create(title='Hello', content='Content Welcome', user=self.user)

        self.create_comment_url = reverse('list-create-post-comment', kwargs={'parent_post_id': self.p.pk})

    def test_create_post_comment_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        data = {
            'body': 'Hello comment here body what is all this.'
        }
        response = self.client.post(self.create_comment_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_comment_unauthenticated(self):
        data = {
            'body': 'Hello comment here body what is all this.'
        }
        client = APIClient()
        response = client.post(self.create_comment_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_comment_comment_authenticated(self):
        comment = Comment.objects.create(user=self.user, body='janudf dfnodsf', parent_post=self.p)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        data = {
            'body': 'Hello comment here body what is all this.'
        }
        url = reverse('list-create-comment-comment',
                      kwargs={'parent_post_id': self.p.id, 'parent_comment_id': comment.id})
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_comment_unauthenticated(self):
        comment = Comment.objects.create(user=self.user, body='janudf dfnodsf', parent_post=self.p)
        data = {
            'body': 'Hello comment here body what is all this.'
        }
        url = reverse('list-create-comment-comment',
                      kwargs={'parent_post_id': self.p.id, 'parent_comment_id': comment.id})
        client = APIClient()
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CommentUpdateTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='neefemee@gmail.com', username='oluwanifemi')
        self.user.set_password('nifemi3')
        self.user.save()

        self.token = Token.objects.get(user=self.user).key
        self.p = Post.objects.create(title='Hello', content='Content Welcome', user=self.user)
        self.c = Comment.objects.create(parent_post=self.p, body='Comment here', user=self.user)
        self.url = reverse('get-comment', kwargs={'parent_post_id': self.p.pk, 'pk': self.c.pk})

    def test_can_update_authenticated(self):
        payload = {
            'body': 'Comment Changed'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.patch(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('body'), 'Comment Changed')

    def test_cannot_update_unauthenticated(self):
        payload = {
            'body': 'Comment Changed'
        }
        response = self.client.patch(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_update_third_party_comment(self):
        user = User.objects.create(email='neefemee2@gmail.com', username='damey')
        user.set_password('nifemi3')
        user.save()
        token = Token.objects.get(user=user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        payload = {
            'body': 'Comment Changed'
        }
        response = self.client.patch(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostUpvoteTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='neefemee@gmail.com', username='oluwanifemi')
        self.user.set_password('nifemi3')
        self.user.save()

        self.token = Token.objects.get(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.p = Post.objects.create(title='Hello', content='Content Welcome', user=self.user)
        self.upvote_url = reverse('upvote-post', kwargs={'pk': self.p.pk})
        self.downvote_url = reverse('downvote-post', kwargs={'pk': self.p.pk})

    def test_can_upvote_authenticated(self):
        response = self.client.post(self.upvote_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_upvote_unauthenticated(self):
        client = APIClient()
        response = client.post(self.upvote_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_remove_upvote(self):
        response = self.client.delete(self.upvote_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_can_downvote_authenticated(self):
        response = self.client.post(self.downvote_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_downvote_unauthenticated(self):
        client = APIClient()
        response = client.delete(self.downvote_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_remove_downvote(self):
        response = self.client.delete(self.upvote_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PostStarTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='neefemee@gmail.com', username='oluwanifemi')
        self.user.set_password('nifemi3')
        self.user.save()

        self.token = Token.objects.get(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.p = Post.objects.create(title='Hello', content='Content Welcome', user=self.user)
        self.star_url = reverse('star-post', kwargs={'pk': self.p.pk})

    def can_list_post_stars(self):
        response = self.client.get(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_star_post_authenticated(self):
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_star_post_unauthenticated(self):
        client = APIClient()
        response = client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_unstar_post_authenticated(self):
        response = self.client.delete(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_unstar_post_unauthenticated(self):
        client = APIClient()
        response = client.delete(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PostFlagTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='neefemee@gmail.com', username='oluwanifemi')
        self.user.set_password('nifemi3')
        self.user.save()

        self.token = Token.objects.get(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.p = Post.objects.create(title='Hello', content='Content Welcome', user=self.user)

        self.payload = {
            "reason": "I dont like him"
        }

        self.flag_url = reverse('flag-post', kwargs={'pk': self.p.pk})

    def can_list_flag_stars(self):
        response = self.client.get(self.flag_url, data=self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_flag_post_authenticated(self):
        response = self.client.post(self.flag_url, data=self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_flag_post_unauthenticated(self):
        client = APIClient()
        response = client.post(self.flag_url, data=self.payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_unflag_post_authenticated(self):
        response = self.client.delete(self.flag_url, data=self.payload)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_unflag_flag_unauthenticated(self):
        client = APIClient()
        response = client.delete(self.flag_url, data=self.payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CommentStarTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='neefemee@gmail.com', username='oluwanifemi')
        self.user.set_password('nifemi3')
        self.user.save()

        self.token = Token.objects.get(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.p = Post.objects.create(title='Hello', content='Content Welcome', user=self.user)
        self.c = Comment.objects.create(parent_post=self.p, user=self.user, body="ndd kdfm")

        self.payload = {
            "reason": "I dont like him"
        }

        self.star_url = reverse('star-comment', kwargs={'pk': self.c.pk, 'parent_post_id': self.p.pk})

    def can_list_comment_stars(self):
        response = self.client.get(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_star_comment_authenticated(self):
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_star_comment_unauthenticated(self):
        client = APIClient()
        response = client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_unstar_comment_authenticated(self):
        response = self.client.delete(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_unstar_comment_unauthenticated(self):
        client = APIClient()
        response = client.delete(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CommentFlagTestCases(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='neefemee@gmail.com', username='oluwanifemi')
        self.user.set_password('nifemi3')
        self.user.save()

        self.token = Token.objects.get(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.p = Post.objects.create(title='Hello', content='Content Welcome', user=self.user)
        self.c = Comment.objects.create(parent_post=self.p, user=self.user, body="ndd kdfm")

        self.payload = {
            "reason": "I dont like him"
        }

        self.flag_url = reverse('flag-comment', kwargs={'pk': self.c.pk, 'parent_post_id': self.p.pk})

    def can_list_comment_stars(self):
        response = self.client.get(self.flag_url, data=self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_star_comment_authenticated(self):
        response = self.client.post(self.flag_url, data=self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_star_comment_unauthenticated(self):
        client = APIClient()
        response = client.post(self.flag_url, data=self.payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_unstar_comment_authenticated(self):
        response = self.client.delete(self.flag_url, data=self.payload)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_unstar_comment_unauthenticated(self):
        client = APIClient()
        response = client.delete(self.flag_url, data=self.payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

