from django.shortcuts import render

from ads.forms import SearchForm
from categories.models import Category


# Create your views here.
def home(request):
    categories = Category.category_manager.active_categories_home()
    form = SearchForm()
    context = {
        'categories': categories,
        'form': form,
    }
    return render(request, 'pages/homepage.html', context)


def terms(response):
    return render(response, "pages/terms_and_conditions.html")


def privacy(response):
    return render(response, "pages/policy_privacy.html")


def cookie(response):
    return render(response, "pages/coockies.html")
