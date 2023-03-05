from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, OuterRef, Subquery
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from ads.models import Announcement
from .forms import MessageForm
from .models import Conversation, Message

User = get_user_model


# Create your views here.
@require_POST
@login_required
def contact_seller(request, ann_id):
    ad = get_object_or_404(Announcement, slug=ann_id, status="AP")
    if ad.profile.user != request.user:
        conversation = Conversation.get_conversation(
            request.user, ad.profile.user,
            subject=f"Has contacted you regarding announcement number: {ad.unique_code}, with title: {ad.title}"
        )
        form = MessageForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.sender = request.user
            new_form.conversation = conversation
            new_form.save()
            messages.add_message(
                request, messages.SUCCESS, 'Your message has been sent successfully.', extra_tags="success"
            )
            return redirect('ads:announcement_detail', ad.slug)
        else:
            messages.add_message(
                request, messages.ERROR, 'There was a problem sending your message, please try again later.',
                extra_tags="danger"
            )
            return redirect('ads:announcement_detail', ad.slug)
    else:
        messages.add_message(
            request, messages.ERROR, 'There was a problem sending your message, please try again later. Type yourself.',
            extra_tags="danger"
        )
        return redirect('ads:announcement_detail', ad.slug)


@login_required
def conversations(request):
    unread_messages_subquery = Message.objects.select_related('conversation').filter(
        conversation=OuterRef('pk'), is_read=False
    ).values(
        'conversation'
    ).exclude(sender=request.user)
    total_unread_messages_subquery = unread_messages_subquery.annotate(count=Count('content')).values('count')
    objects_list = Conversation.objects.filter(participants=request.user).annotate(
        unread_messages=Subquery(total_unread_messages_subquery))
    context = {
        'objects_list': objects_list,
    }
    return render(request, 'chat/inbox.html', context)


@transaction.atomic
@login_required
def get_conversation(request, conv_id):
    conversation = get_object_or_404(Conversation, id=conv_id, participants=request.user)
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    objects_list = Conversation.objects.filter(participants=request.user)
    form = MessageForm(request.POST)
    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.sender = request.user
        new_form.conversation = conversation
        new_form.save()
        return redirect("chat:get_conversation", conversation.id)
    context = {
        'conversation': conversation,
        'objects_list': objects_list,
        'form': form,
    }
    return render(request, 'chat/conversation.html', context)
