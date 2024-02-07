from django.test import TestCase
from django.contrib.auth.models import User
from posts.models import Tags, Images, Posts
from users.models import Profile
from datetime import datetime


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

        existing_posts = Posts.objects.filter(user=self.profile)

        if existing_posts.exists():
            self.posts = existing_posts
        else:
            self.posts = Posts.objects.create(
                user=self.profile,
                date=datetime.now(),
                comments='This is a test comments.'
            )

            self.image = Images.objects.create(
                image='path/to/test_image.png'
            )

            self.tags = Tags.objects.create(
                tags='#test'
            )

            self.posts.tags.add(self.tags)
            self.posts.images.add(self.image)

    def test_profile_creation(self):
        self.assertTrue(isinstance(self.profile, Profile))
        self.assertEqual(str(self.profile), self.user.username)

    def test_post_creation(self):
        self.assertTrue(isinstance(self.posts, Posts))
        self.assertEqual(self.posts.user, self.profile)
        self.assertEqual(self.posts.comments, 'This is a test comments.')
        self.assertEqual(self.posts.images.count(), 1)

    def test_post_tags(self):
        self.assertEqual(self.posts.tags.count(), 1)
        self.assertEqual(str(self.posts.tags.first()), '#test')





