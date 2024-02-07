from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from posts.forms import CreatePost, CreateImage, CreateTags


class FormsTestCase(TestCase):
    def test_create_post_form(self):
        form_data = {'user_id': '2183', 'comments': 'test'}
        form = CreatePost(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})

    def test_create_image_form(self):
        form_data = {'image': SimpleUploadedFile('test_image.jpg', b'content')}
        form = CreateImage(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})

    def test_create_tag_form(self):
        form_data = {'tags': '#test'}
        form = CreateTags(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})
