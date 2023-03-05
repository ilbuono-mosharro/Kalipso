from django import template

register = template.Library()


@register.filter
def calculate_percentage(count, total):
    if count and total:
        return round(int(count) / int(total) * 100)
    else:
        return 0
