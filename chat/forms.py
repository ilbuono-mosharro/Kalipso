from django import forms
from django.forms import Textarea

from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)

        widgets = {
            'content': Textarea(attrs={'class': 'form-control', 'rows': "3", 'placeholder': "Write your message"})
        }

    def clean_content(self):
        content = self.cleaned_data['content']
        if not all(content.isalnum() or content.isspace() or content in [',', '.', '-', "'", '(', ')', '"']
                   for content in content):
            raise forms.ValidationError(
                'This field can only contain letters, numbers and ,.-"()')
        return content
