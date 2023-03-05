from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Category

@login_required
def categories_list(request):
    categories = Category.category_manager.active_categories()
    context = {
        'categories': categories,
    }
    return render(request, 'categories/list.html', context)
