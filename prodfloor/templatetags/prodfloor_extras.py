from django import template
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

register = template.Library()

@register.simple_tag()
def getpercentage(A, B, *args, **kwargs):
    return ((A+1) / B)*100

@register.simple_tag()
def session(session_key,*args, **kwargs):
    ss = SessionStore(session_key=session_key)
    ss['already_here']=False
    s = Session.objects.get(pk=session_key)
    print(s.get_decoded())


