from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse


class TestViewsCalls(TestCase):
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
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)

    def test_sign_out_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_profile_view(self):
        response = self.client.get(reverse('profile', kwargs={'user_id': '2183'}))
        self.assertEqual(response.status_code, 302)

    def test_profile_settings_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile_settings'))
        self.assertEqual(response.status_code, 302)

