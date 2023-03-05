from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.forms import Select, TextInput, NumberInput, RadioSelect, CheckboxInput
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import User, Individual, Company, Profile
from .token import token_generator


class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg mb-2', 'placeholder': 'Username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control form-control-lg mb-2', 'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control form-control-lg mb-2', 'placeholder': 'Password confirmation'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control form-control-lg', 'placeholder': 'Enter your email'
        })
        self.fields['terms_and_privacy'].widget.attrs.update({'class': 'form-check-input'})

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'u_type', 'terms_and_privacy']
        widgets = {
            'u_type': RadioSelect({'class': 'list-group-item-check pe-none'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('That username is already taken.')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password_mismatch.')
        return password2

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email

    def send_activation_email(self, request, user):
        current_site = get_current_site(request)
        subject = 'Activate Your Account'
        message = render_to_string(
            'accounts/email_activation.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            }
        )

        user.email_user(subject, message, html_message=message)


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("There is no guest registered with the specified email address!")
        return email


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        widgets = {
            'first_name': TextInput(attrs={
                'class': 'form-control form-control-lg', 'placeholder': 'First Name', 'required': 'required'
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control form-control-lg', 'placeholder': 'Last Name', 'required': 'required'
            }),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not all(first_name.isalpha() or first_name.isspace() for first_name in first_name):
            raise forms.ValidationError('This field can only contain letters.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not all(last_name.isalpha() or last_name.isspace() for last_name in last_name):
            raise forms.ValidationError('This field can only contain letters.')
        return last_name


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs.update({
            'class': 'form-control form-control-lg', 'accept': '.jpg, .jpeg, .png'
        })

    class Meta:
        model = Profile
        fields = ('city', 'avatar', 'phone', 'hidden_phone', 'age')

        widgets = {
            'city': Select(attrs={'class': 'form-select form-select-lg select-field', 'placeholder': 'City'}),
            'phone': NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Phone Number'}),
            'hidden_phone': CheckboxInput(attrs={'class': 'form-check-input'}),
            'age': NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Age'}),
        }

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old to register.")
        else:
            if age > 99:
                raise forms.ValidationError("Check that you have entered your age correctly.")
        return age


class IndividualProfileForm(UserProfileForm):
    class Meta:
        model = Individual
        fields = UserProfileForm.Meta.fields + ('gender',)

        widgets = {
            **UserProfileForm.Meta.widgets,
            'gender': Select(attrs={'class': 'form-select form-select-lg select-field', 'placeholder': 'Gender'}),
        }


class CompanyProfileForm(UserProfileForm):
    class Meta:
        model = Company
        fields = ('name', 'vat_number', 'address', 'zip_code') + UserProfileForm.Meta.fields

        widgets = {
            **UserProfileForm.Meta.widgets,
            'name': TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Company Name'}),
            'vat_number': TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Vat Number'}),
            'address': TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Address'}),
            'zip_code': NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Zip Code'}),
        }

        labels = {
            'name': 'Company Name',
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Company.objects.filter(name__iexact=name).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('That company name is already taken.')
        return name

    def clean_vat_number(self):
        vat_number = self.cleaned_data['vat_number']
        if Company.objects.filter(vat_number__iexact=vat_number).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('That Vat Number name is already taken.')
        return vat_number

    def clean_address(self):
        address = self.cleaned_data['address']
        if not all(address.isalnum() or address.isspace() or address in [',', '.', '-', "'", '(', ')', '"']
                   for address in address):
            raise forms.ValidationError(
                'This field can only contain letters, numbers and ,.-"()')
        return address
