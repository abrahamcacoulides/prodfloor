from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('home.urls', namespace="home")),
    url(r'^prodfloor/', include('prodfloor.urls', namespace="prodfloor")),
    url(r'^admin/', admin.site.urls),
    url('^', include('django.contrib.auth.urls')),
    url('^accounts/', include('django.contrib.auth.urls')),
]
