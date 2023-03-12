from django.test import TestCase
from ..forms import RegistrationForm
from ..models import User


class RegistrationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="test1", password="testpassword1", email="test1@test.com", u_type="CO",
                                 terms_and_privacy=True, ip="192.168.1.125")

    def test_u_type_co_label(self):
        form = RegistrationForm()
        u_type = form.fields['u_type']
        self.assertTrue(u_type.label is None or u_type.label == "U type")
        self.assertEqual(u_type.choices[1][1], "Company")
        self.assertEqual(u_type.choices[2][1], "Individual Person")

    def test_terms_and_privacy(self):
        form = RegistrationForm()
        self.assertTrue(form.fields['terms_and_privacy'].label == "Terms and privacy")

    def test_validation_username(self):
        form = RegistrationForm(data={
            'username': "test1", 'password1': "passwordtest", 'password2': "passwordtest", 'email': 'test@gmail.com',
            'u_type': "CO", 'terms_and_privacy': True
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'username': ["That username is already taken."]})
