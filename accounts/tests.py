from django.test import TestCase
from django.urls import reverse

from .forms import RegistrationForm
from .models import User


class UserModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="testuser1", password="testpassword", email="test@test.com",
                                        u_type="CO",
                                        terms_and_privacy=True, ip="192.168.1.155")

    def test_user_data(self):
        self.assertEqual(self.user.username, "testuser1")
        self.assertEqual(self.user.password, "testpassword")


class RegistrationFormTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="testuser1", password="testpassword", email="test@test.com",
                                        u_type="CO", terms_and_privacy=True, ip="192.168.1.155")

    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'u_type': 'CO',
            'terms_and_privacy': True,
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_username_taken(self):
        form_data = {
            'username': self.user,
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'u_type': 'CO',
            'terms_and_privacy': True,
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('That username is already taken.', form.errors['username'])

    def validate_fields_form(self):
        form_data = {
            'username': "/sdd*sd*dss*d",
            'email': '/sdd*sd*dss*d',
            'password1': '/sdd*sd*dss*d',
            'password2': 'testpassword',
            'u_type': 'CO',
            'terms_and_privacy': True,
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password2', form.errors)


class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser1", password="testpassword", email="test@test.com",
                                             u_type="CO", terms_and_privacy=True, ip="192.168.1.155")
        self.client.login(username='testuser', password='testpass')

    def test_user_wishlist_view(self):
        url = reverse('accounts:user_wishlist')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
