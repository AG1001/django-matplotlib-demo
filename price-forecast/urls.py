"""price-forecast URL Configuration."""

from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
  url(r'^admin/', include(admin.site.urls)),
  url(r'forecast/', include('forecast.urls')),
  url(r'^$', include('forecast.urls')),
]
