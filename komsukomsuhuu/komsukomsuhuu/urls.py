from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
import profiles.views
import groups.views
import entities.views
import messages.views
import notifications

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url('^inbox/notifications/', include(notifications.urls)),
    url(r'', include('user_sessions.urls', 'user_sessions')),

    # profile processes
    url(r'^register', profiles.views.register, name='register'),
    url(r'^login', profiles.views.login, name='login'),
    url(r'^logout', profiles.views.logout, name='logout'),
    url(r'^edit_profile', profiles.views.edit_profile, name='edit_profile'),
    url(r'^mark_as_read/$', entities.views.mark_as_read, name='mark_as_read'),
    url(r'^notifications', profiles.views.notifications, name='notifications'),
    #password reset
    url(r'^password/reset/$',
        'django.contrib.auth.views.password_reset',
        {'post_reset_redirect':'/password/reset/done/'},
        name='password_reset'),

    url(r'^password/reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        name='password_reset_done'),

    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect':'/password/done/'},
        name='password_reset_confirm'),

    url(r'^password/done/$',
        'django.contrib.auth.views.password_reset_complete',
        name='password_reset_complete'),
    # other
    url(r'^$', 'profiles.views.home', name='home'),
    url(r'^users/(?P<username>[\w\._-]+)$', profiles.views.users, name='users'),
    url(r'^profile/', profiles.views.user_profile, name='profile'),

    #group processes
    url(r'groups', groups.views.list_groups, name='groups'),
    url(r'new_group', groups.views.new_group, name='new_group'),
    url(r'^delete_group/(?P<pk>[\d]+)$', groups.views.delete_group, name='delete_group'),
    url(r'^detail_group/(?P<pk>[\d]+)$', groups.views.detail_group, name='detail_group'),
    url(r'^edit_group/(?P<pk>[\d]+)$', groups.views.edit_group, name='edit_group'),
    url(r'^join_group/(?P<pk>[\d]+)$', groups.views.join_group, name='join_group'),
    url(r'^fav_group/(?P<pk>[\d]+)$', groups.views.favorite_group, name='fav_group'),
    url(r'maps', groups.views.list_groups_on_map, name='maps'),
    url(r'show_neighbours', groups.views.show_neighbours, name='show_neighbours'),

    #entities

    url(r'new_topic/(?P<pk>[\d]+)$', entities.views.new_topic, name='new_topic'),
    url(r'^detail_topic/(?P<pk>[\d]+)$', entities.views.detail_topic, name='detail_topic'),
    url(r'^new_post/(?P<pk>[\d]+)$', entities.views.new_post, name='new_post'),
    url(r'^fav_topic/(?P<pk>[\d]+)$', entities.views.favorite_topic, name='fav_topic'),
    url(r'show_topics', entities.views.show_topics, name='show_topics'),

    #messages

    url(r'^users/(?P<username>[\w\._-]+)/new-message$', messages.views.new_message, name='new_message'),
    url(r'^messages$', messages.views.inbox, name='inbox'),
    url(r'^messages/(?P<pk>[\d]+)$', messages.views.conversation_detail, name='conversation_detail'),

    #search
    url(r'search', profiles.views.search, name='search'),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                            document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                            document_root=settings.MEDIA_ROOT)
