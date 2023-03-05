from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from ads.models import Announcement
from reviews.forms import ReviewForm
from reviews.models import ReviewRating
from .decorators import authentication_not_required
from .forms import RegistrationForm, UserUpdateForm, IndividualProfileForm, CompanyProfileForm
from .models import Profile
from .token import token_generator

User = get_user_model()


# Create your views here.
@authentication_not_required
def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.ip = request.META.get('REMOTE_ADDR')
            user.is_active = False
            user.save()
            form.send_activation_email(request, user)
            return redirect('accounts:info_account_activation')
        else:
            messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                                 extra_tags="danger")
    else:
        form = RegistrationForm()
    return render(request, 'accounts/sign-up.html', {'form': form, 'section': 'sign_up'})


@authentication_not_required
def info_account_activation(request):
    return render(request, 'accounts/message_activation_account.html')


@authentication_not_required
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.email_confirmation = True
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Your account has been confirmed successfully.',
                             extra_tags='success')
        return redirect('login')
    else:
        return render(request, 'accounts/email_activation_invalid.html')


def get_percentage_field_with_value(*forms):
    fields_with_value = len([field.value() for form in forms for field in form if field.value()])
    total_fields = sum(len(form.fields) for form in forms)
    percentage = round(fields_with_value / total_fields * 100)
    return percentage


@login_required
def update_profile(request):
    profile_form = None
    user = request.user
    individual = User.UserTypeChoice.INDIVIDUAL
    company = User.UserTypeChoice.COMPANY
    percentage = 0
    if request.method == 'POST':
        form_u = UserUpdateForm(request.POST, instance=user, prefix="user_form")

        if user.u_type == individual:
            profile_form = IndividualProfileForm(request.POST, request.FILES,
                                                 instance=user.user_profile_related.individual,
                                                 prefix="individual_form")
        elif user.u_type == company:
            profile_form = CompanyProfileForm(request.POST, request.FILES, instance=user.user_profile_related.company,
                                              prefix="company_form")

        if form_u.is_valid() and profile_form and profile_form.is_valid():
            profile = profile_form.save(commit=False)
            user = form_u.save(commit=False)
            user.ip = request.META.get('REMOTE_ADDR')
            user.save()
            profile.is_complete = True
            profile.save()
            messages.add_message(request, messages.SUCCESS, 'Data updated successfully.')
            return redirect('accounts:update_profile')
        else:
            messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                                 extra_tags='danger')
    else:
        form_u = UserUpdateForm(instance=user, prefix="user_form")

        if user.u_type == individual:
            profile_form = IndividualProfileForm(instance=user.user_profile_related.individual,
                                                 prefix="individual_form")
        elif user.u_type == company:
            profile_form = CompanyProfileForm(instance=user.user_profile_related.company, prefix="company_form")
        percentage = get_percentage_field_with_value(form_u, profile_form)
    return render(request, 'accounts/dashboard/profile.html',
                  {'form_u': form_u, 'profile_form': profile_form, 'section': 'profile', 'percentage': percentage})


@login_required
def delete_user(request):
    user = get_object_or_404(User, is_active=True, username=request.user)
    if request.method == 'POST':
        user.ip = request.META.get('REMOTE_ADDR')
        user.is_active = False
        user.save()
        logout(request)
        messages.add_message(request, messages.ERROR, 'Your account has been successfully deactivated.',
                             extra_tags='danger')
        return redirect('logout')
    else:
        messages.add_message(request, messages.ERROR,
                             'Your account has not been deactivated because a problem has occurred, '
                             'to deactivate it contact us via email.', extra_tags='danger', )
        return redirect('accounts:update_profile')


@login_required
def user_ads(request):
    announcements = Announcement.ad_manager.active_ad().filter(profile__user=request.user)
    context = {
        'announcements': announcements,
        'section': 'user_ads',
    }
    return render(request, 'accounts/dashboard/ads.html', context)


@login_required
def user_wishlist(request):
    announcements = Announcement.ad_manager.active_ad().filter(users_wishlist=request.user)
    context = {
        'announcements': announcements,
        'section': 'user_wish',
    }
    return render(request, 'accounts/dashboard/wishlist.html', context)


@login_required
def user_reviews(request):
    reviews_about_you = ReviewRating.objects.filter(profile__user=request.user).select_related(
        'profile', 'user', 'profile__individual', 'profile__company'
    )
    reviews_by_you = ReviewRating.objects.filter(user=request.user).select_related(
        'profile', 'user', 'profile__individual', 'profile__company'
    )
    context = {
        'reviews_about_you': reviews_about_you,
        'reviews_by_you': reviews_by_you,
        'section': 'user_review',
    }
    return render(request, 'accounts/dashboard/reviews.html', context)


@login_required
def update_review(request, review_id):
    review = get_object_or_404(ReviewRating, id=review_id, user=request.user)
    if request.method == "POST":
        form = ReviewForm(request.POST or None, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.ip = request.META.get('REMOTE_ADDR')
            review.user = request.user
            review.save()
            messages.add_message(request, messages.SUCCESS, 'Review update successufy.', extra_tags="success")
            return redirect('accounts:user_reviews')
        else:
            messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                                 extra_tags="danger")
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/update_review.html', {'form': form, 'review': review})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(ReviewRating, id=review_id, user=request.user)
    if request.method == "POST":
        review.delete()
        messages.add_message(request, messages.SUCCESS, 'Review deleted successufy.', extra_tags="success")
    else:
        messages.add_message(request, messages.ERROR, 'Your rating could not be deleted, please try again later.',
                             extra_tags="danger")
    return redirect('accounts:user_reviews')


def public_profile(request, unique_code):
    profile = get_object_or_404(Profile.objects.select_related(
        'user', 'city', 'individual', 'company'
    ), unique_code=unique_code, user__is_active=True)
    announcements = profile.announcement_user_profile.select_related(
        'profile', 'category', 'subcategory', 'city', 'standard', 'standard__auto', 'standard__moto', 'jobs',
        'properties', 'properties__house', 'profile__user'
    ).prefetch_related(
        'users_wishlist', 'announcement_images',
    ).filter(status="AP")
    reviews = profile.review_profile.select_related('profile', 'user').filter(status="AP")
    reviews_data = profile.review_profile.select_related('profile', 'user').filter(status="AP").values(
        'rating'
    ).annotate(count=Count('rating')).order_by('-rating')
    form = None
    user_review_exists = None
    if request.user.is_authenticated:
        user_review_exists = profile.review_profile.filter(user=request.user).exists()
        if request.method == 'POST' and not user_review_exists:
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                review = form.save(commit=False)
                review.ip = request.META.get('REMOTE_ADDR')
                review.profile = profile
                review.user = request.user
                review.save()
                messages.add_message(request, messages.SUCCESS, 'Your review will be published in a few minutes.',
                                     extra_tags='success')
                return redirect('accounts:public_profile', profile.unique_code)
            else:
                messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                                     extra_tags="danger")
        else:
            form = ReviewForm()
    return render(request, 'accounts/public_profile.html', {'profile': profile, 'announcements': announcements,
                                                            'reviews': reviews, 'reviews_data': reviews_data,
                                                            'form': form, "user_review_exists": user_review_exists})
