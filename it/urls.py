from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from it import views
from .views import *

urlpatterns = [
    url(r'^documentstop/', views.Temp, name='temp'),
    #url(r'^documentstop/(?P<number>[0-9]{1})',login_required(ServerStop.as_view(ServerStop.form_list))),
]