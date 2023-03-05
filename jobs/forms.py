from django.forms import Select

from ads.forms import AdsForm
from .models import Jobs


class JobAdsForm(AdsForm):
    class Meta:
        model = Jobs
        fields = AdsForm.Meta.fields + ('schedule', 'level')

        widgets = {
            **AdsForm.Meta.widgets,  # => Python 3.5
            'level': Select(attrs={'class': 'form-select form-select-lg select-field', 'placeholder': 'Level'}),
            'schedule': Select(attrs={'class': 'form-select form-select-lg select-field', 'placeholder': 'Schedule'}),
        }


class UpdateJobAdsForm(JobAdsForm):
    class Meta:
        model = Jobs
        fields = JobAdsForm.Meta.fields + ('category', 'subcategory',)

        widgets = {
            **JobAdsForm.Meta.widgets,  # => Python 3.5
            'category': Select(attrs={'class': 'form-select form-select-lg select-field', 'placeholder': 'Category'}),
            'subcategory': Select(
                attrs={'class': 'form-select form-select-lg select-field', 'placeholder': 'Subcategory'}),
        }
