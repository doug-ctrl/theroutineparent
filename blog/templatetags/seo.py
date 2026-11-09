from django import template
from django.conf import settings
from django.utils.encoding import escape_uri_path

register = template.Library()


@register.filter
def apex_url(obj):
    """Absolute apex URL for any object with get_absolute_url."""
    return settings.SITE_URL + obj.get_absolute_url()


@register.simple_tag(takes_context=True)
def canonical_url(context):
    """Apex URL for the current path, plus ?page=N only for page 2 onwards.

    All other query params (utm_*, fbclid, q, ...) are dropped.
    """
    request = context.get("request")
    path = escape_uri_path(request.path) if request else "/"
    url = settings.SITE_URL + path
    page_obj = context.get("page_obj")
    if page_obj and page_obj.number > 1:
        url += f"?page={page_obj.number}"
    return url
