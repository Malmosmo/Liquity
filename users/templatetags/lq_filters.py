from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def download(value: str):
    value = value.replace(" ", "")
    return value.lower()
