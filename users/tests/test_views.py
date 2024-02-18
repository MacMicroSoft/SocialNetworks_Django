from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, Client
from django.urls import reverse
from users.models import Profile

class TestViewsCalls(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        if not hasattr(self.user, 'profile'):
            self.profile = Profile.objects.create(user=self.user)
        else:
            self.profile = self.user.profile

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_sign_up_view(self):
        response = self.client.post(reverse('register'),
                                    {'username': 'newuser',
                                     'password1': 'newpassword123',
                                     'password2': 'newpassword123',
                                     'email': 'newuser@example.com'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)

    def test_sign_in_view(self):
        response = self.client.post(reverse('login'), {'username': 'john', 'password': 'johnpassword'}, follow=True)
        self.assertRedirects(response, reverse('profile', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)

    def test_sign_out_view(self):
        response = self.client.get(reverse('logout'), {'username': 'john', 'password': 'johnpassword'})
        self.assertEqual(response.status_code, 302)

    def test_profile_view(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('profile', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)

    def test_profile_settings_view(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('profile_settings'))
        self.assertEqual(response.status_code, 200)

    def test_profile_followers_view(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('followers', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)

    def test_profile_follow_delete_view(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.post(reverse('follow', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)

    def test_profile_follow_view(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('follow', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
