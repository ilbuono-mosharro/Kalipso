from django.forms import NumberInput, RadioSelect, Select

from ads.forms import AdsForm
from .models import Properties, House


class PropertiesAdsForm(AdsForm):
    class Meta:
        model = Properties
        fields = AdsForm.Meta.fields + ('square_feet', 'ad_type',)

        widgets = {
            **AdsForm.Meta.widgets,  # => Python 3.5
            'square_feet': NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Square feet'}),
            'ad_type': RadioSelect(attrs={'class': 'form-check-input', 'placeholder': 'Type'}),
        }


class UpdatePropertiesAdsForm(PropertiesAdsForm):
    class Meta:
        model = Properties
        fields = PropertiesAdsForm.Meta.fields + ('category', 'subcategory',)

        widgets = {
            **PropertiesAdsForm.Meta.widgets,  # => Python 3.5
            'category': Select(attrs={'class': 'form-select form-select-lg select-field', 'placeholder': 'Category'}),
            'subcategory': Select(
                attrs={'class': 'form-select form-select-lg select-field', 'placeholder': 'Subcategory'}),
        }


class HouseAdsForm(PropertiesAdsForm):
    class Meta:
        model = House
        fields = PropertiesAdsForm.Meta.fields + ('bedrooms', 'bathrooms',)

        widgets = {
            **PropertiesAdsForm.Meta.widgets,  # => Python 3.5
            'bedrooms': NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Bedrooms'}),
            'bathrooms': NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Bathrooms'}),
        }


class UpdateHouseAdsForm(HouseAdsForm):
    class Meta:
        model = House
        fields = HouseAdsForm.Meta.fields + ('category', 'subcategory',)

        widgets = {
            **HouseAdsForm.Meta.widgets,  # => Python 3.5
            'category': Select(attrs={'class': 'form-select form-select-lg select-field', 'placeholder': 'Category'}),
            'subcategory': Select(
                attrs={'class': 'form-select form-select-lg select-field', 'placeholder': 'Subcategory'}),
        }
