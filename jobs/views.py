from django.contrib.auth.decorators import login_required

from accounts.decorators import profile_complete_required
from ads.views import add_announcement, update_announcement
from .forms import JobAdsForm, UpdateJobAdsForm
from .models import Jobs


# Create your views here.
@login_required
@profile_complete_required
def add_announcement_job(request, category_id, subcat_id):
    return add_announcement(request, category_id, subcat_id, JobAdsForm, "add_job")


@login_required
@profile_complete_required
def update_announcement_job(request, ann_id):
    return update_announcement(request, Jobs, ann_id, UpdateJobAdsForm, 'update_job_ad')
