import functools

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def authentication_not_required(view_func, redirect_url="pages:home"):
    """
        this decorator ensures that a user is not logged in,
        if a user is logged in, the user will get redirected to
        the url whose view name was passed to the redirect_url parameter
    """

    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, 'You need to be logged out')
        return redirect(redirect_url)
    return wrapper


def ajax_login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def profile_complete_required(view_func, redirect_url='accounts:update_profile'):
    @functools.wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        profile = request.user.user_profile_related
        if not profile.is_complete:
            messages.add_message(request, messages.INFO, 'You need to complete your profile before add a new ad.')
            return redirect(redirect_url)
        return view_func(request, *args, **kwargs)
    return wrapped_view
