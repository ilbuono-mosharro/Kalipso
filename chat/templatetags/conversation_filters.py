from django import template

register = template.Library()


@register.filter
def other_participant(conversation, user):
    """Returns the other participant in the conversation."""
    return conversation.get_other_participant(user)
