from django import forms
from django.forms import TextInput, FileInput, Select, NumberInput, Textarea, CheckboxInput

from engines.models import Auto
from jobs.models import Jobs
from .models import Standard, Image, Cities, Announcement
from .utils import PRICE_LIST, SORTING_LIST, CategoryChoiceField


class SearchForm(forms.Form):
    keyword_q = forms.CharField(max_length=30, required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control text-white border-color-cs w-768', 'placeholder': "Search for title, keyword, etc."
        }))
    categories = CategoryChoiceField(widget=forms.Select(
        attrs={"class": "form-select flex-fill-cs select-field w-768"}
    ), required=False)
    cities = forms.ModelChoiceField(queryset=Cities.city_manager.active_cities(), empty_label="All cities",
                                    widget=forms.Select(attrs={"class": "form-select flex-fill-cs select-field w-768"}),
                                    required=False)
    condition = forms.ChoiceField(choices=Standard.ConditionTypeChoice.choices, required=False,
                                  widget=forms.HiddenInput)
    transmissions = forms.ChoiceField(choices=Auto.TransmissionTypeChoice.choices, required=False,
                                      widget=forms.HiddenInput)
    fuels = forms.ChoiceField(choices=Auto.FuelTypeChoice.choices, required=False, widget=forms.HiddenInput)
    ad_types = forms.ChoiceField(choices=Auto.AdTypeChoice.choices, required=False, widget=forms.HiddenInput)
    schedules = forms.ChoiceField(choices=Jobs.JobScheduleChoice.choices, required=False, widget=forms.HiddenInput)
    levels = forms.ChoiceField(choices=Jobs.JobLevelChoice.choices, required=False, widget=forms.HiddenInput)
    price_min = forms.ChoiceField(choices=PRICE_LIST, widget=forms.HiddenInput, required=False)
    price_max = forms.ChoiceField(choices=PRICE_LIST, widget=forms.HiddenInput, required=False)
    sorting = forms.ChoiceField(choices=SORTING_LIST, required=False, widget=forms.HiddenInput, initial="-created_at")

    def clean_keyword_q(self):
        keyword_q = self.cleaned_data['keyword_q']
        if not all(k.isalnum() or k.isspace() for k in keyword_q):
            raise forms.ValidationError("You can only search by letters and numbers.")
        return keyword_q


class AdsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdsForm, self).__init__(*args, **kwargs)
        self.fields['city'].empty_label = "Select a city"

    class Meta:
        model = Announcement
        fields = ('title', 'description', 'city', 'price')

        widgets = {
            'title': TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Title'}),
            'description': Textarea(attrs={'class': 'form-control form-control-lg h-25', 'placeholder': 'Description'}),
            'city': Select(attrs={'class': 'form-select form-select-lg select-field', 'placeholder': 'City'}),
            'price': NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Price'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if not all(title.isalnum() or title.isspace() for title in title):
            raise forms.ValidationError(
                'This field can only contain letters and numbers.')
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        if not all(description.isalnum() or description.isspace() or description in [',', '.', '-', "'", '(', ')', '"']
                   for description in description):
            raise forms.ValidationError(
                'This field can only contain letters, numbers and ,.-"()')
        return description


class StandardAdsForm(AdsForm):
    class Meta:
        model = Standard
        fields = AdsForm.Meta.fields + ('condition',)

        widgets = {
            **AdsForm.Meta.widgets,  # => Python 3.5
            'condition': Select(attrs={'class': 'form-select form-select-lg select-field', 'placeholder': 'Condition'}),
        }


class UpdateStandardAdsForm(StandardAdsForm):
    class Meta:
        model = Standard
        fields = StandardAdsForm.Meta.fields + ('category', 'subcategory',)

        widgets = {
            **StandardAdsForm.Meta.widgets,  # => Python 3.5
            'category': Select(attrs={'class': 'form-select form-select-lg select-field', 'placeholder': 'Category'}),
            'subcategory': Select(attrs={'class': 'form-select form-select-lg select-field', 'placeholder': 'Subcategory'}),
        }

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', 'alt_text', 'is_active')

        widgets = {
            'alt_text': TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'image': FileInput(attrs={'class': 'form-control', 'accept': '.jpg, .jpeg, .png'}),
            'is_active': CheckboxInput(attrs={'class': 'form-check-input'}),
        }


