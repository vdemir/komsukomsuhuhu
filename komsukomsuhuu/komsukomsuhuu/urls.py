from django.conf.urls import patterns, include, url
from django.contrib import admin
import profiles.views
import groups.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # authenticate processes
    url(r'^register', profiles.views.register, name='register'),
    url(r'^login', profiles.views.login, name='login'),
    url(r'^logout', profiles.views.logout, name='logout'),
    # other
    url(r'^$', 'profiles.views.home', name='home'),
    url(r'groups', groups.views.list_groups, name='groups'),
    url(r'new_group', groups.views.new_group, name='new_group'),
    url(r'^delete_group/(?P<pk>[\d]+)$', groups.views.delete_group, name='delete_group'),
    url(r'^detail_group/(?P<pk>[\d]+)$', groups.views.detail_group, name='detail_group'),
    url(r'^edit_group/(?P<pk>[\d]+)$', groups.views.edit_group, name='edit_group'),
    url(r'^join_group/(?P<pk>[\d]+)$', groups.views.join_group, name='join_group'),
)


