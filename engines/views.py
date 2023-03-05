from django.contrib.auth.decorators import login_required

from accounts.decorators import profile_complete_required
from ads.views import add_announcement, update_announcement
from engines.forms import AutoAdsForm, MotoAdsForm, UpdateAutoAdsForm, UpdateMotoAdsForm
from .models import Auto, Moto


# Create your views here.
@login_required
@profile_complete_required
def add_announcement_auto(request, category_id, subcat_id):
    return add_announcement(request, category_id, subcat_id, AutoAdsForm, "add_auto")


@login_required
@profile_complete_required
def update_announcement_auto(request, ann_id):
    return update_announcement(request, Auto, ann_id, UpdateAutoAdsForm, 'update_auto_ad')


@login_required
@profile_complete_required
def add_announcement_moto(request, category_id, subcat_id):
    return add_announcement(request, category_id, subcat_id, MotoAdsForm, "add_moto")


@login_required
@profile_complete_required
def update_announcement_moto(request, ann_id):
    return update_announcement(request, Moto, ann_id, UpdateMotoAdsForm, 'update_moto_ad')
