from django.test import TestCase
from users.forms import LoginForm, ProfileForm, UpdateUserForm, UserCreationForm, RegisterForm


class FormsTestCase(TestCase):
    def test_login_form(self):
        form_data = {'username': 'testuser', 'password': 'testpassword'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form(self):
        form_data = {'username': 'newuser', 'email': 'newuser@example.com', 'password1': 'newpassword123',
                     'password2': 'newpassword123'}
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_profile_form(self):
        form_data = {'bio': 'Updated bio', 'avatar': 'path/to/updated_avatar.jpg'}
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_update_user_form(self):
        form_data = {'first_name': 'Updated', 'last_name': 'User'}
        form = UpdateUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_form_invalid_passwords(self):
        form_data = {'username': 'newuser', 'email': 'newuser@example.com', 'password1': 'password123',
                     'password2': 'differentpassword'}
        form = RegisterForm(data=form_data)
        form.is_valid()
        self.assertFalse(form.is_valid())
