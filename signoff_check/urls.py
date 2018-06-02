from django.conf.urls import url

from . import views

app_name = 'signoff_check'
urlpatterns = [
	url(r'^$',views.index, name='index'),
	url(r'^test/$',views.index, name='test'),
	url(r'^r0/$',views.index, name='r0'),
	url(r'^r1/$',views.another_stage, name='r1'),
	url(r'^another_stage/$',views.another_stage, name='another_stage'),
	url(r'^(?P<pk>[0-9]+)/owner/$',views.owner, name='owner'),
	url(r'^(?P<pk>[0-9]+)/(?P<path_id>[0-9]+)/path/$',views.path, name='path'),
	url(r'^(?P<pk>[0-9]+)/group/$',views.group, name='group'),
	url(r'^(?P<pk>[0-9]+)/(?P<path_id>[0-9]+)/group_path/$',views.group_path, name='group_path'),
	url(r'^vclp/$',views.vclp, name='vclp'),
	url(r'^(?P<pk>[0-9]+)/(?P<vtag>[\w]+)/tag/(?P<check_item>[\w]+)/$',views.tag, name='tag'),
	url(r'^(?P<pk>[0-9]+)/(?P<vtag>[\w]+)/vclp_case/$',views.vclp_case, name='vclp_case'),
	url(r'^(?P<partition>[\w]+)/(?P<corner>[\w/]+)/(?P<signoff_mode>[\w]+)/(?P<check_mode>[\w]+)/partition_status/$',views.parition_status, name='partition_status'),
	url(r'^other_check/$',views.other_check, name='other_check'),
	url(r'^(?P<partition>[\w]+)/(?P<corner>[\w/]+)/(?P<signoff_mode>[\w]+)/$',views.other_check_status, name='other_check_status'),
	#url(r'^(?P<partition>[\w]+)/(?P<corner>[\w/]+)/(?P<signoff_mode>[\w]+)/(?P<check>[\w]+)/update_comment$',views.update_comment, name='update_comment'),
	url(r'^(?P<pk>[0-9]+)/update_comment$',views.update_comment, name='update_comment'),
    url(r'^login/$',views.login, name='login'),
    url(r'^logout/$',views.logout, name='logout'),
    url(r'^password_change/$',views.password_change, name='password_change'),
    url(r'^password_change/done/$', views.password_change_done, name='password_change_done'),
	]

