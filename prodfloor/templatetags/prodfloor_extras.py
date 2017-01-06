from django import template

register = template.Library()

@register.simple_tag()
def getpercentage(A, B, *args, **kwargs):
    return ((A+1) / B)*100