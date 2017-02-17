from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.admin.sites import AdminSite

urlpatterns = [
    url(r'^', include('home.urls', namespace="home")),
    url(r'^prodfloor/', include('prodfloor.urls', namespace="prodfloor")),
    url(r'^it/', include('it.urls', namespace="it")),
    url(r'^admin/', admin.site.urls),
    url('^', include('django.contrib.auth.urls')),
    url('^accounts/', include('django.contrib.auth.urls')),
]

AdminSite.index_title = "ProdFloor HUB"
AdminSite.site_header = "ProdFloor Administration"