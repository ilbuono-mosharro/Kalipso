from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from ..forms import RegistrationForm, IndividualProfileForm, UserUpdateForm, CompanyProfileForm
from ..models import User
from ..token import token_generator


class RegistrationTestCase(TestCase):

    def test_form_and_template_used(self):
        response = self.client.get(path=reverse("accounts:sign_up"))
        self.assertIsInstance(response.context['form'], RegistrationForm)
        self.assertTemplateUsed(response, 'accounts/sign-up.html')

    def test_sign_up(self):
        data = {
            'username': "test1",
            'password1': "test1password",
            'password2': "test1password",
            'email': "test@test.com",
            "u_type": "CO",
            "terms_and_privacy": True,
        }

        response = self.client.post(path=reverse('accounts:sign_up'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("accounts:info_account_activation"))

        self.assertTrue(User.objects.filter(username="test1").exists())

        user = User.objects.get(username='test1')
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.ip, '127.0.0.1')
        self.assertFalse(user.is_active)

        self.assertEqual(len(mail.outbox), 1)
        activation_email = mail.outbox[0]
        self.assertEqual(activation_email.to, ['test@test.com'])
        self.assertIn('Activate Your Account', activation_email.subject)

    def test_sign_up_unsuccessful(self):
        data = {
            'username': "test1/*//*//**--+",
            'password1': "test1password",
            'password2': "test1password1",
            'email': "test@test.com",
            "u_type": "CO",
            "terms_and_privacy": True,
        }
        form = RegistrationForm(data=data)
        response = self.client.post(path=reverse("accounts:sign_up"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            form, 'username',
            "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters."
        )
        self.assertFormError(form, 'password2', "Password_mismatch.")
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'Please fill in all fields correctly and try again.')


class TestInfoAccountActivation(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="test1", password="testpassword", ip="192.168.1.125", u_type="CO",
                                 terms_and_privacy=True)

    def test_template_used(self):
        response = self.client.get(path=reverse("accounts:info_account_activation"))
        self.assertTemplateUsed(response, "accounts/message_activation_account.html")

    def test_redirect_user_authenticated(self):
        self.client.login(username="test1", password="testpassword")
        response = self.client.get(path=reverse("accounts:info_account_activation"))
        self.assertRedirects(response, reverse("pages:home"))


class TestActivateAccount(TestCase):
    def test_activation_success(self):
        user = User.objects.create_user(username="test1", password="testpassword", ip="192.168.1.125", u_type="CO",
                                        terms_and_privacy=True)
        token = token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        response = self.client.get(reverse('accounts:activate_account', args=[uidb64, token]))
        self.assertEqual(response.status_code, 302)  # Expect redirect to login page
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertTrue(user.email_confirmation)

    def test_activation_invalid(self):
        response = self.client.get(reverse('accounts:activate_account', args=['invalid_uidb64', 'invalid_token']))
        self.assertEqual(response.status_code, 200)


class TestUpdateProfile(TestCase):
    def setUp(self):
        self.individual = User.objects.create_user(username="test1", password="testpassword", ip="192.168.1.125",
                                                   u_type="PE", terms_and_privacy=True)
        self.company = User.objects.create_user(username="test2", password="testpassword", ip="192.168.1.125",
                                                u_type="CO", terms_and_privacy=True)

    def test_form_and_template_used_individual_authenticate(self):
        self.client.login(username="test1", password="testpassword")
        response = self.client.get(path=reverse('accounts:update_profile'))
        self.assertIsInstance(response.context['form_u'], UserUpdateForm)
        self.assertEqual(response.context['form_u'].prefix, 'user_form')
        self.assertIsInstance(response.context['profile_form'], IndividualProfileForm)
        self.assertEqual(response.context['profile_form'].prefix, 'individual_form')
        self.assertTemplateUsed(response, 'accounts/dashboard/profile.html')

    def test_form_and_template_used_company_authenticate(self):
        self.client.login(username="test2", password="testpassword")
        response = self.client.get(path=reverse('accounts:update_profile'))
        self.assertIsInstance(response.context['form_u'], UserUpdateForm)
        self.assertIsInstance(response.context['profile_form'], CompanyProfileForm)
        self.assertEqual(response.context['profile_form'].prefix, 'company_form')
        self.assertTemplateUsed(response, 'accounts/dashboard/profile.html')

    def test_update_data_individual(self):
        data = {
            'user_form-first_name': "Marco",
            'user_form-last_name': "Mario",
            # 'individual_form-city': "290b63dc-247a-4a64-8da7-58413f484cc1",
            'individual_form-phone': "000000000",
            "individual_form-age": 20,
            "individual_form-hidden_phone": True,
            "individual_form-gender": "ML",
        }

        self.client.login(username="test1", password="testpassword")
        response = self.client.post(path=reverse("accounts:update_profile"), data=data)
        self.assertEqual(response.status_code, 302)
        updated_user = User.objects.get(username=self.individual.username)
        self.assertEqual(updated_user.first_name, "Marco")
        self.assertEqual(updated_user.last_name, "Mario")
        self.assertEqual(updated_user.ip, '127.0.0.1')
        self.assertEqual(updated_user.user_profile_related.phone, "000000000")
        self.assertEqual(updated_user.user_profile_related.age, 20)
        self.assertEqual(updated_user.user_profile_related.hidden_phone, True)
        self.assertEqual(updated_user.user_profile_related.individual.gender, "ML")
        self.assertTrue(updated_user.user_profile_related.is_complete)

    def test_update_data_company(self):
        data = {
            'user_form-first_name': "Marco",
            'user_form-last_name': "Mario",
            # 'individual_form-city': "290b63dc-247a-4a64-8da7-58413f484cc1",
            'company_form-phone': "000000000",
            "company_form-age": 18,
            "company_form-hidden_phone": False,
            "company_form-name": "Test Inc",
            'company_form-vat_number': 'L5485485',
            'company_form-address': 'londra',
            'company_form-zip_code': '0025',
        }

        self.client.login(username="test2", password="testpassword")
        response = self.client.post(path=reverse("accounts:update_profile"), data=data)
        self.assertEqual(response.status_code, 302)
        updated_user = User.objects.get(username=self.company.username)
        self.assertEqual(updated_user.first_name, "Marco")
        self.assertEqual(updated_user.last_name, "Mario")
        self.assertEqual(updated_user.ip, '127.0.0.1')
        self.assertEqual(updated_user.user_profile_related.phone, "000000000")
        self.assertEqual(updated_user.user_profile_related.age, 18)
        self.assertEqual(updated_user.user_profile_related.hidden_phone, False)
        self.assertEqual(updated_user.user_profile_related.company.name, "Test Inc")
        self.assertEqual(updated_user.user_profile_related.company.vat_number, "L5485485")
        self.assertEqual(updated_user.user_profile_related.company.address, "londra")
        self.assertEqual(updated_user.user_profile_related.company.zip_code, "0025")
        self.assertTrue(updated_user.user_profile_related.is_complete)
