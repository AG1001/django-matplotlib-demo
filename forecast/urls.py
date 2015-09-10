from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
  url(r'^predict/', views.forecast),
  url(r'^plot_img/(\w*),(\w)',views.plot_img, name='plot_img'),
  url(r'^$', views.index, name='index'),
)
