from django.conf.urls import url

from . import views

app_name = 'vp_web'
urlpatterns = [
	url(r'^$',views.index, name='index'),
	url(r'^index$',views.index, name='index'),
	url(r'^(?P<pk>[0-9]+)/index_status/$',views.index_status, name='index_status'),
	url(r'^(?P<feature_id>[0-9]+)/feature/$',views.feature, name='feature'),
	url(r'^(?P<pk>[0-9]+)/component/$',views.component, name='component'),
	url(r'^(?P<pk>[0-9]+)/point/$',views.point, name='point'),
	url(r'^(?P<pk>[0-9]+)/add_feature/$',views.add_feature, name='add_feature'),
	url(r'^(?P<pk>[0-9]+)/change_feature/$',views.change_feature, name='change_feature'),
	url(r'^(?P<pk>[0-9]+)/add_verification/$',views.add_verification, name='add_verification'),
	url(r'^(?P<pk>[0-9]+)/change_verification/$',views.change_verification, name='change_verification'),
	url(r'^login/$',views.login, name='login'),
	url(r'^(?P<pk>[0-9]+)/workspace/$',views.workspace, name='workspace'),
	url(r'^(?P<pk>[0-9]+)/review/$',views.review, name='review'),
	url(r'^(?P<pk>[0-9]+)/status_list/$',views.status_list, name='status_list'),
	url(r'^(?P<pk>[0-9]+)/component_status_list/$',views.component_status_list, name='component_status_list'),
	url(r'^logout/$',views.logout, name='logout'),
    url(r'^password_change/$',views.password_change, name='password_change'),
    url(r'^password_change/done/$', views.password_change_done, name='password_change_done'),
	url(r'^cross_check/$',views.display_cross_check_result, name='cross_check'),
	url(r'^register_status/$',views.display_class_register_result, name='register_status'),
	url(r'^cross_check_update/$',views.cross_check_update, name='cross_check_update'),
	url(r'^coverage_trace/$',views.coverage_trace, name='coverage_trace'),
	url(r'^coverage_count/$',views.coverage_count, name='coverage_count'),
	url(r'^(?P<pk>[0-9]+)/(?P<type>[\w]+)/cross_check/$',views.cross_check_result_by_owner, name='cross_check_result_by_owner'),
	url(r'^vrg_app/$',views.vrg_app, name='vrg_app'),
	url(r'^lint_app/$',views.lint_app, name='lint_app'),
	url(r'^signoff_app/$',views.signoff_app, name='signoff_app'),
	url(r'^gazer/$',views.gazer, name='gazer'),
	url(r'^about/$',views.about, name='about'),
	]
