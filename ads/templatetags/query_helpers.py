from django import template
from django.http import QueryDict

register = template.Library()


@register.simple_tag
def relative_url(
        param_key: str,
        param_value: str,
        querydict: QueryDict = None
) -> str:
    """
    Construct and return a query params string.
    Arguments passed to this function take
    precedence over any existing query param
    for a request.
    """
    # QueryDicts are immutable by default.
    new_querydict = QueryDict(mutable=True)
    new_querydict.appendlist(param_key, param_value)

    if not querydict:
        # No existing query params in the URL, so we're done.
        # We just needed to append the args that were
        # passed to this function.
        return f"?{new_querydict.urlencode()}"
    else:
        # This means there are some existing params in the URL.
        # We'd like to append them now and return that URL.
        # At the same time, we want to ensure that the
        # param_key and param_value passed to the function
        # take precedence over the one in the URL.
        # That happens when we check for key != param_key.
        for key, value in querydict.items():
            if key != param_key:
                new_querydict.appendlist(key, value)
        return f"?{new_querydict.urlencode()}"
