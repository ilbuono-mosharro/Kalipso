from django.contrib.auth.decorators import login_required

from accounts.decorators import profile_complete_required
from ads.views import add_announcement, update_announcement
from .forms import PropertiesAdsForm, HouseAdsForm, UpdatePropertiesAdsForm, UpdateHouseAdsForm
from .models import Properties, House


# Create your views here.
@login_required
@profile_complete_required
def add_announcement_property(request, category_id, subcat_id):
    return add_announcement(request, category_id, subcat_id, PropertiesAdsForm, "add_property")


@login_required
@profile_complete_required
def update_announcement_property(request, ann_id):
    return update_announcement(request, Properties, ann_id, UpdatePropertiesAdsForm, 'update_property_ad')


@login_required
@profile_complete_required
def add_announcement_apartments(request, category_id, subcat_id):
    return add_announcement(request, category_id, subcat_id, HouseAdsForm, "add_apartments")


@login_required
@profile_complete_required
def update_announcement_apartments(request, ann_id):
    return update_announcement(request, House, ann_id, UpdateHouseAdsForm, 'update_apartments_ad')
