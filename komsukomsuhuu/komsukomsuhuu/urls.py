from django.conf.urls import patterns, include, url
from django.contrib import admin
import profiles.views


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
)


