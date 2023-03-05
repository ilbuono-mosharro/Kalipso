from django.contrib import admin
from .models import Conversation, Message

# Register your models here.

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    def get_participants(self, obj):
        return ", ".join([str(p) for p in obj.participants.all()])

    list_display = ('get_participants', 'subject', "timestamp")
    list_filter = ('participants',)
    search_fields = ('subject', 'participants')
    list_per_page = 20
    ordering = ('-timestamp',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'content', 'is_read',)
    list_filter = ('conversation', 'sender',)
    search_fields = ('conversation', 'sender', 'content',)
    list_per_page = 20
    ordering = ('-timestamp',)
