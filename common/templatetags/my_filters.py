from django import template
from django.utils.encoding import force_unicode

register = template.Library()

@register.filter
def in_group(user, group):
    return bool(user.groups.filter(name__iexact=group))