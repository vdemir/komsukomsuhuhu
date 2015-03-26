from django.conf.urls import patterns, include, url
from django.contrib import admin
import profiles.views
import groups.views
import entities.views


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    # profile processes
    url(r'^register', profiles.views.register, name='register'),
    url(r'^login', profiles.views.login, name='login'),
    url(r'^logout', profiles.views.logout, name='logout'),
    url(r'^edit_profile', profiles.views.edit_profile, name='edit_profile'),
    # other
    url(r'^$', 'profiles.views.home', name='home'),
    #group processes
    url(r'groups', groups.views.list_groups, name='groups'),
    url(r'new_group', groups.views.new_group, name='new_group'),
    url(r'^delete_group/(?P<pk>[\d]+)$', groups.views.delete_group, name='delete_group'),
    url(r'^detail_group/(?P<pk>[\d]+)$', groups.views.detail_group, name='detail_group'),
    url(r'^edit_group/(?P<pk>[\d]+)$', groups.views.edit_group, name='edit_group'),
    url(r'^join_group/(?P<pk>[\d]+)$', groups.views.join_group, name='join_group'),
    url(r'^fav_group/(?P<pk>[\d]+)$', groups.views.favorite_group, name='fav_group'),

    #entities

    url(r'new_topic/(?P<pk>[\d]+)$', entities.views.new_topic, name='new_topic'),
    url(r'^detail_topic/(?P<pk>[\d]+)$', entities.views.detail_topic, name='detail_topic'),
    url(r'^new_post/(?P<pk>[\d]+)$', entities.views.new_post, name='new_post'),
    url(r'^fav_topic/(?P<pk>[\d]+)$', entities.views.favorite_topic, name='fav_topic'),

)


