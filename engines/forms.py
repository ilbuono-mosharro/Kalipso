from django import forms
from django.forms import TextInput, Select, NumberInput, RadioSelect

from ads.forms import StandardAdsForm
from .models import Auto, Moto


class AutoAdsForm(StandardAdsForm):
    class Meta:
        model = Auto
        fields = StandardAdsForm.Meta.fields + ('make', 'doors', 'seats', 'fuel', 'transmission', 'consumption',
                                                'ad_type', 'kms_driven', 'first_registration', 'drive_type')

        widgets = {
            **StandardAdsForm.Meta.widgets,  # => Python 3.5
            'make': TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Make'}),
            'doors': Select(attrs={'class': 'form-select form-select-lg select-field', 'placeholder': 'Doors'}),
            'seats': NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Seats'}),
            'fuel': Select(attrs={'class': 'form-select form-select-lg select-field', 'placeholder': 'Fuel'}),
            'transmission': Select(attrs={
                'class': 'form-select form-select-lg select-field', 'placeholder': 'Transmission'
            }),
            'ad_type': RadioSelect(attrs={'class': 'form-check-input', 'placeholder': 'Type'}),
            'consumption': TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Consumption'}),
            'kms_driven': NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Kms driven'}),
            'first_registration': TextInput(
                attrs={'class': 'form-control form-control-lg', 'placeholder': 'First registration'}),
            'drive_type': Select(attrs={
                'class': 'form-select form-select-lg select-field', 'placeholder': 'Drive type'
            }),
        }

    def clean_make(self):
        make = self.cleaned_data['make']
        if not all(make.isalnum() or make.isspace() for make in make):
            raise forms.ValidationError(
                'This field can only contain letters and numbers.')
        return make

    def clean_doors(self):
        doors = self.cleaned_data['doors']
        if not all(doors.isdigit() or doors.isspace() or doors == "/" for doors in doors):
            raise forms.ValidationError(
                'This field can only contain letters and numbers.')
        return doors

    def clean_consumption(self):
        consumption = self.cleaned_data['consumption']
        if not all(consumption.isalnum() or consumption.isspace() or consumption == "/" for consumption in consumption):
            raise forms.ValidationError(
                'This field can only contain letters and numbers.')
        return consumption

    def clean_first_registration(self):
        first_registration = self.cleaned_data['first_registration']
        if not all(first_registration.isalnum() or first_registration.isspace() or first_registration == "/"
                   for first_registration in first_registration):
            raise forms.ValidationError(
                'This field can only contain letters and numbers.')
        return first_registration

    def clean_drive_type(self):
        drive_type = self.cleaned_data['drive_type']
        if not all(drive_type.isalnum() or drive_type.isspace() for drive_type in drive_type):
            raise forms.ValidationError(
                'This field can only contain letters and numbers.')
        return drive_type


class MotoAdsForm(StandardAdsForm):
    class Meta:
        model = Moto
        fields = StandardAdsForm.Meta.fields + ('make', 'fuel', 'transmission', 'consumption', 'condition', 'ad_type',
                                                'kms_driven', 'first_registration',)

        widgets = {
            **StandardAdsForm.Meta.widgets,  # => Python 3.5
            'make': TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Make'}),
            'fuel': Select(attrs={'class': 'form-select form-select-lg select-field', 'placeholder': 'Fuel'}),
            'transmission': Select(attrs={
                'class': 'form-select form-select-lg select-field', 'placeholder': 'Transmission'
            }),
            'condition': Select(attrs={
                'class': 'form-select form-select-lg select-field', 'placeholder': 'Select condition'
            }),
            'ad_type': RadioSelect(attrs={'class': 'form-check-input', 'placeholder': 'Type'}),
            'consumption': TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Consumption'}),
            'kms_driven': NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Kms driven'}),
            'first_registration': TextInput(attrs={
                'class': 'form-control form-control-lg', 'placeholder': 'First registration'
            }),
        }

    def clean_make(self):
        make = self.cleaned_data['make']
        if not all(make.isalnum() or make.isspace() for make in make):
            raise forms.ValidationError(
                'This field can only contain letters and numbers.')
        return make

    def clean_consumption(self):
        consumption = self.cleaned_data['consumption']
        if not all(consumption.isalnum() or consumption.isspace() or consumption == "/" for consumption in consumption):
            raise forms.ValidationError(
                'This field can only contain letters and numbers.')
        return consumption

    def clean_first_registration(self):
        first_registration = self.cleaned_data['first_registration']
        if not all(first_registration.isalnum() or first_registration.isspace() or first_registration == "/"
                   for first_registration in first_registration):
            raise forms.ValidationError(
                'This field can only contain letters and numbers.')
        return first_registration


class UpdateAutoAdsForm(AutoAdsForm):
    class Meta:
        model = Auto
        fields = AutoAdsForm.Meta.fields + ('category', 'subcategory',)
        widgets = {
            **AutoAdsForm.Meta.widgets,  # => Python 3.5
            'category': Select(attrs={'class': 'form-select form-select-lg select-field', 'placeholder': 'Category'}),
            'subcategory': Select(
                attrs={'class': 'form-select form-select-lg select-field', 'placeholder': 'Subcategory'}),
        }


class UpdateMotoAdsForm(MotoAdsForm):
    class Meta:
        model = Moto
        fields = MotoAdsForm.Meta.fields + ('category', 'subcategory',)
        widgets = {
            **MotoAdsForm.Meta.widgets,  # => Python 3.5
            'category': Select(attrs={'class': 'form-select form-select-lg select-field', 'placeholder': 'Category'}),
            'subcategory': Select(
                attrs={'class': 'form-select form-select-lg select-field', 'placeholder': 'Subcategory'}),
        }
