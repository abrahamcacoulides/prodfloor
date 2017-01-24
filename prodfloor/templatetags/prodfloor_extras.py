from django import template
from django.contrib.sessions.models import Session

register = template.Library()

@register.simple_tag()
def getpercentage(A, B, *args, **kwargs):
    return ((A+1) / B)*100

@register.simple_tag()
def properUser(*args, **kwargs):
    pass

