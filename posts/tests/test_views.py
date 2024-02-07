from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from posts.models import Posts, Tags


class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_posts_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('create_posts'))
        self.assertEqual(response.status_code, 200)

    def test_posts_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('posts'))
        self.assertEqual(response.status_code, 200)

    def test_user_posts_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('user_posts'))
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_view(self):
        self.client.login(username='testuser', password='testpassword')
        post = Posts.objects.create(user=self.user.profile)
        response = self.client.get(reverse('edit_profile', args=[post.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_like_view(self):
        self.client.login(username='testuser', password='testpassword')
        post = Posts.objects.create(user=self.user.profile)
        response = self.client.get(reverse('post_like', args=[post.id]))
        self.assertEqual(response.status_code, 302)
