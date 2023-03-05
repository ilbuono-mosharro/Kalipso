import uuid

from django.conf import settings
from django.db import models


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    subject = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Conversation {self.id}'

    class Meta:
        ordering = ('-id',)

    def get_other_participant(self, user):
        """Returns the other participant in the conversation."""
        return self.participants.exclude(id=user.id).first()

    @classmethod
    def get_conversation(cls, user1, user2, subject):
        """Returns the conversation between two users if it exists, otherwise creates it."""
        conversation = cls.objects.filter(participants=user1).filter(participants=user2).first()
        if not conversation:
            conversation = cls.objects.create(subject=subject)
            conversation.participants.add(user1, user2)
        return conversation


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message {self.id}'
