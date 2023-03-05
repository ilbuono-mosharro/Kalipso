from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ReviewForm
from .models import ReviewRating


# Create your views here.

@login_required
def modify_review(request, review_id):
    review = get_object_or_404(ReviewRating, id=review_id, user=request.user)
    if request.method == "POST":
        form = ReviewForm(request.POST or None, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.subject = form.cleaned_data['subject']
            review.review = form.cleaned_data['review']
            review.rating = form.cleaned_data['rating']
            review.ip = request.META.get('REMOTE_ADDR')
            review.user = request.user
            review.save()
            messages.add_message(request, messages.SUCCESS, 'Review update successufy.', extra_tags="success")
            return redirect('pages:reviews_dashboard')
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
        messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                             extra_tags="danger")
    return redirect('pages:reviews_dashboard')
