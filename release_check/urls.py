from django.conf.urls import url

from . import views

app_name = 'release_check'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<pk>[0-9]+)/owner/$', views.owner, name='owner'),
	url(r'^(?P<pk>[0-9]+)/log/$', views.log, name='log'),
	]
