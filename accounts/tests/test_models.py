from django.test import TestCase
from ..models import User, Company, Individual, Profile
from cities.models import Cities


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="test1", password="testpassword1", email="test1@test.com", u_type="CO",
                                 terms_and_privacy=True, ip="192.168.1.125")
        User.objects.create_user(username="test2", password="testpassword1", email="test1@test.com", u_type="PE",
                                 terms_and_privacy=True, ip="192.168.1.125")

    def test_u_type_label(self):
        user = User.objects.get(username="test1")
        field_label = user._meta.get_field('u_type').verbose_name
        self.assertEqual(field_label, "u type")

    def test_terms_and_privacy_label(self):
        user = User.objects.get(username="test1")
        field_label = user._meta.get_field('terms_and_privacy').verbose_name
        self.assertEqual(field_label, "terms and privacy")

    def test_ip_label(self):
        user = User.objects.get(username="test1")
        field_label = user._meta.get_field('ip').verbose_name
        self.assertEqual(field_label, 'ip')

    def test_u_type_max_length(self):
        user = User.objects.get(username="test1")
        max_length = user._meta.get_field('u_type').max_length
        self.assertEqual(max_length, 20)

    def test_u_type_choices_and_label(self):
        user_co = User.objects.get(username="test1")
        user_pe = User.objects.get(username="test2")
        if user_co.u_type == "CO":
            company = user_co._meta.get_field('u_type').choices[0][1]
            self.assertEqual(company, "Company")
        elif user_pe.u_type == "PE":
            individual_person = user_pe._meta.get_field('u_type').choices[1][1]
            self.assertEqual(individual_person, "Individual Person")


class IndividualModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="test3", password="testpassword1", email="test1@test.com",
                                              u_type="PE", terms_and_privacy=True, ip="192.168.1.125")
        city = Cities.objects.create(user=user, name="Tirana")
        Profile.objects.create(user_id=user.id, city=city)


    def test_user_label(self):
        individual = Profile.objects.get(user__username="test3")
        field_label = individual._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')
s





