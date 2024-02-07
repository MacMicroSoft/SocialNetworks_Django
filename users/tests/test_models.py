from django.contrib.auth.models import User
from django.test import TestCase

from users.models import Profile


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')

    def setUp(self):
        self.user = User.objects.get(username='testuser')

        existing_profile = Profile.objects.filter(user=self.user).first()

        if existing_profile:
            self.profile = existing_profile
        else:
            self.profile = Profile.objects.create(
                user=self.user,
                avatar='path/to/test_avatar.png',
                bio='This is a test bio.'
            )

    def test_get_absolute_url(self):
        self.assertEqual(self.profile.get_absolute_url(), self.profile.avatar.url)

    def test_bio_max_length(self):
        max_length = self.profile._meta.get_field('bio').max_length
        self.assertEqual(max_length, 255)
