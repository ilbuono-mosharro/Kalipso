import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect

from accounts.decorators import profile_complete_required
from categories.models import Category, SubCategory
from chat.forms import MessageForm
from .forms import SearchForm, StandardAdsForm, ImageForm, UpdateStandardAdsForm
from .models import Announcement, Image, Standard


# Create your views here.
#
def is_valid_queryparam(param):
    return param != '' and param is not None


def announcements(request):
    subcategory = None
    category_f = None
    objects_list = Announcement.ad_manager.active_ad()
    form = SearchForm(request.GET)
    if form.is_valid():
        keyword_q = form.cleaned_data['keyword_q']
        category = form.cleaned_data['categories']
        city = form.cleaned_data['cities']
        condition = form.cleaned_data['condition']
        sorting = form.cleaned_data['sorting']
        transmission = form.cleaned_data['transmissions']
        fuel = form.cleaned_data['fuels']
        ad_type = form.cleaned_data['ad_types']
        schedule = form.cleaned_data['schedules']
        level = form.cleaned_data['levels']
        price_min = form.cleaned_data['price_min']
        price_max = form.cleaned_data['price_max']
        subcategory = SubCategory.objects.filter(slug=category, is_active=True).only(
            'filter_transmissions', 'filter_fuels', 'filter_ad_types', 'filter_price_min', 'filter_price_max',
            'filter_schedules', 'filter_levels', 'filter_condition',
        ).first()
        category_f = Category.objects.filter(slug=category, is_active=True).only(
            'filter_transmissions', 'filter_fuels', 'filter_ad_types', 'filter_price_min', 'filter_price_max',
            'filter_schedules', 'filter_levels', 'filter_condition',
        ).first()
        if is_valid_queryparam(keyword_q):
            objects_list = objects_list.filter(
                Q(title__icontains=keyword_q) | Q(description__icontains=keyword_q)
            )
        if is_valid_queryparam(city):
            objects_list = objects_list.filter(
                Q(city__exact=city)
            )
        if is_valid_queryparam(sorting):
            objects_list = objects_list.order_by(
                sorting
            )
        if is_valid_queryparam(category):
            objects_list = objects_list.filter(
                Q(subcategory__slug__exact=category) | Q(category__slug__exact=category)
            )
        if subcategory and subcategory.filter_transmissions or category_f and category_f.filter_transmissions:
            if is_valid_queryparam(transmission):
                objects_list = objects_list.filter(
                    Q(standard__auto__transmission__exact=transmission) | Q(
                        standard__moto__transmission__exact=transmission)
                )
        if subcategory and subcategory.filter_fuels or category_f and category_f.filter_fuels:
            if is_valid_queryparam(fuel):
                objects_list = objects_list.filter(
                    Q(standard__auto__fuel__exact=fuel) | Q(standard__moto__fuel__exact=fuel)
                )
        if subcategory and subcategory.filter_ad_types or category_f and category_f.filter_ad_types:
            if is_valid_queryparam(ad_type):
                objects_list = objects_list.filter(
                    Q(standard__auto__ad_type__exact=ad_type) | Q(standard__moto__ad_type__exact=ad_type) |
                    Q(properties__ad_type__exact=ad_type) | Q(properties__house__ad_type__exact=ad_type)
                )
        if subcategory and subcategory.filter_price_min or category_f and category_f.filter_price_min:
            if is_valid_queryparam(price_min):
                objects_list = objects_list.filter(
                    price__gte=price_min
                )
        if subcategory and subcategory.filter_price_max or category_f and category_f.filter_price_max:
            if is_valid_queryparam(price_max):
                objects_list = objects_list.filter(
                    price__lte=price_max
                )
        if subcategory and subcategory.filter_schedules or category_f and category_f.filter_schedules:
            if is_valid_queryparam(schedule):
                objects_list = objects_list.filter(
                    Q(jobs__schedule__exact=schedule)
                )
        if subcategory and subcategory.filter_levels or category_f and category_f.filter_levels:
            if is_valid_queryparam(level):
                objects_list = objects_list.filter(
                    Q(jobs__level__exact=level)
                )
        if subcategory and subcategory.filter_condition or category_f and category_f.filter_condition:
            if is_valid_queryparam(condition):
                objects_list = objects_list.filter(
                    Q(standard__condition__exact=condition) | Q(standard__auto__condition__exact=condition)
                    | Q(standard__moto__condition__exact=condition)
                )
    paginator = Paginator(objects_list, 10)  # Show 1 contacts per page.
    page_number = request.GET.get('page')
    announcement = paginator.get_page(page_number)
    return render(request, 'ads/list.html', {
        'announcements': announcement, 'form': form,
        'subcategory': subcategory, "category_f": category_f
    })


def categories_and_sub(request, category_slug=None, sabcategory_slug=None):
    category = None
    subcategory = None
    objects_list = Announcement.ad_manager.active_ad()
    form = SearchForm()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        objects_list = objects_list.filter(category=category.id)
        form.initial = {'categories': category.slug}
    if category_slug and sabcategory_slug:
        subcategory = get_object_or_404(
            SubCategory, category__slug=category_slug, slug=sabcategory_slug, is_active=True
        )
        objects_list = objects_list.filter(subcategory=subcategory.id)
        form.initial = {'categories': subcategory.slug}
    paginator = Paginator(objects_list, 1)  # Show 1 contacts per page.
    page_number = request.GET.get('page')
    announcement = paginator.get_page(page_number)
    return render(request, 'categories/ann_by_cat_and_sub.html', {'category': category, 'subcategory': subcategory,
                                                                  'announcements': announcement, 'form': form})


def announcement_detail(request, slug):
    announcement = get_object_or_404(Announcement.ad_manager.active_ad(), slug=slug)  # is_active=True
    form = MessageForm()
    cookie_name = f'visited-{announcement.slug}'
    # Using cookie
    if not request.COOKIES.get(f'visited-{announcement.slug}'):
        request.COOKIES[f'visited-{announcement.slug}'] = True

        # Using session
        # if not request.session.get(f'visited-{announcement.id}'):
        #     request.session[f'visited-{announcement.id}'] = True

        announcement.visits += 1
        announcement.save()
    context = {
        'announcement': announcement,
        'form': form,
    }

    response = render(request, 'ads/detail.html', context)
    response.set_cookie(cookie_name, True, max_age=24 * 60 * 60)
    return response


@login_required
@profile_complete_required
def add_announcement(request, category_id, subcat_id, form_class, section):
    category = get_object_or_404(Category, id=category_id, is_active=True)
    sub_category = get_object_or_404(SubCategory, id=subcat_id, is_active=True)

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            add_form = form.save(commit=False)
            add_form.category = category
            add_form.subcategory = sub_category
            add_form.profile = request.user.user_profile_related
            add_form.ip = request.META.get('REMOTE_ADDR')
            add_form.save()
            messages.add_message(request, messages.SUCCESS, 'Your ad will be published in a few minutes.',
                                 extra_tags="success")
            return redirect('ads:add_image_announcement', add_form.id)
        else:
            messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                                 extra_tags="danger")
    else:
        form = form_class()

    context = {
        'form': form,
        'category': category,
        'sub_category': sub_category,
        'section': section,
    }

    return render(request, 'ads/add_ad.html', context)


@login_required
@profile_complete_required
def add_standard_announcement(request, category_id, subcat_id):
    return add_announcement(request, category_id, subcat_id, StandardAdsForm, "add_standard")


@login_required
@profile_complete_required
def update_announcement(request, model_name, ann_id, form_class, section):
    announcement = get_object_or_404(model_name, id=ann_id, profile__user=request.user)
    if request.method == 'POST':
        form = form_class(request.POST, instance=announcement)
        if form.is_valid():
            add_form = form.save(commit=False)
            add_form.profile = request.user.user_profile_related
            add_form.ip = request.META.get('REMOTE_ADDR')
            add_form.save()
            messages.add_message(request, messages.SUCCESS, 'Your ad will be updated in a few minutes.',
                                 extra_tags="success")
            return redirect('accounts:user_ads')
        else:
            messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                                 extra_tags="danger")
    else:
        form = form_class(instance=announcement)

    context = {
        'form': form,
        'section': section,
    }

    return render(request, 'ads/update_ad.html', context)


@login_required
@profile_complete_required
def update_standard_announcement(request, ann_id):
    return update_announcement(request, Standard, ann_id, UpdateStandardAdsForm, 'update_standard_ad')


@login_required
@profile_complete_required
def delete_announcement(request, ann_id):
    announcement = get_object_or_404(Announcement, id=ann_id, profile__user=request.user)
    if request.method == "POST":
        announcement.delete()
        messages.add_message(request, messages.SUCCESS, 'Announcement deleted successufy.', extra_tags="success")
    else:
        messages.add_message(request, messages.ERROR, 'The announcement could not be deleted, please try again later.',
                             extra_tags="danger")
    return redirect('accounts:user_ads')


@login_required
@profile_complete_required
def change_status_announcement(request, ann_id):
    announcement = get_object_or_404(Announcement, id=ann_id, profile__user=request.user)
    status = "activated"
    if request.method == "POST":
        if announcement.status == "AP":
            announcement.status = "DE"
            status = "deactivated"
        elif announcement.status == "DE":
            announcement.status = 'AP'
        else:
            messages.add_message(request, messages.ERROR,
                                 'You have to wait for an ad to be approved before you can change the status.',
                                 extra_tags="danger")
        announcement.save(update_fields=['status'])
        messages.add_message(request, messages.SUCCESS, f'The ad has been successfully {status}.',
                             extra_tags="success")
        return redirect('accounts:user_ads')
    else:
        messages.add_message(request, messages.ERROR, 'There was an error, please try again later.',
                             extra_tags="danger")
    return redirect('accounts:user_ads')


@login_required
@profile_complete_required
def add_image_announcement(request, ad_id):
    announcement = get_object_or_404(Announcement, id=ad_id, profile=request.user.user_profile_related)
    if request.method == "POST":
        form = ImageForm(request.POST or None, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.ip = request.META.get('REMOTE_ADDR')
            image.announcement = announcement
            image.profile = request.user.user_profile_related
            image.save()
            messages.add_message(request, messages.SUCCESS, 'Image added successufy.', extra_tags="success")
            return redirect('ads:add_image_announcement', announcement.id)
        else:
            messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                                 extra_tags="danger")
    else:
        form = ImageForm()
    return render(request, 'ads/add_image.html', {'announcement': announcement, 'form': form})


@login_required
@profile_complete_required
def delete_image_announcement(request, image_id):
    image = get_object_or_404(Image, id=image_id, profile=request.user.user_profile_related)
    if request.method == "POST":
        image.delete()
        messages.add_message(request, messages.SUCCESS, 'Image deleted successufy.', extra_tags="success")
    else:
        messages.add_message(request, messages.ERROR, 'The image could not be deleted, please try again later.',
                             extra_tags="danger")
    return redirect('ads:add_image_announcement', image.announcement.id)


@login_required
@profile_complete_required
def modify_image_announcement(request, image_id):
    image = get_object_or_404(Image, id=image_id, profile=request.user.user_profile_related)
    if request.method == "POST":
        form = ImageForm(request.POST or None, request.FILES, instance=image)
        if form.is_valid():
            image = form.save(commit=False)
            image.ip = request.META.get('REMOTE_ADDR')
            image.profile = request.user.user_profile_related
            image.save()
            messages.add_message(request, messages.SUCCESS, 'Image modifidy successufy.', extra_tags="success")
            return redirect('ads:add_image_announcement', image.announcement.id)
        else:
            messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                                 extra_tags="danger")
    else:
        form = ImageForm(instance=image)
    return render(request, 'ads/modify_image.html', {'image': image, 'form': form})


@login_required
def ann_wishlist(request, announcement_id=None):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax and request.user.is_authenticated:
        if request.method == 'POST':
            data = json.load(request)
            ann_id = data.get('ann_id')
            announcement = get_object_or_404(Announcement, id=ann_id)
            if announcement.users_wishlist.filter(id=request.user.id).exists():
                announcement.users_wishlist.remove(request.user)
                return JsonResponse({'status': False})
            else:
                announcement.users_wishlist.add(request.user)
                return JsonResponse({'status': True})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')
