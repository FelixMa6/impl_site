from django.conf.urls import url

from . import views

app_name = 'regression'
urlpatterns = [
	url(r'^$',views.index, name='index'),
	url(r'^(?P<user_id>[0-9]+)/user/$',views.user, name='user'),
	url(r'^(?P<bug_id>[0-9]+)/vector/$',views.vector, name='vector'),
	url(r'^(?P<bug_id>[0-9]+)/log/$',views.logshow, name='log'),
	url(r'^(?P<bug_id>[0-9]+)/wave/$',views.waveshow, name='wave'),
	url(r'^(?P<bug_id>[0-9]+)/src/$',views.srcshow, name='src'),
	url(r'^login/$',views.login, name='login'),
	url(r'^report/$',views.report, name='report'),
	url(r'^passrate/$',views.passrate, name='passrate'),
	url(r'^logout/$',views.logout, name='logout'),
    url(r'^password_change/$',views.password_change, name='password_change'),
            url(r'^password_change/done/$', views.password_change_done,
                name='password_change_done'),
	]