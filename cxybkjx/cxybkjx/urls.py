from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from cxybkjx import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cxybkjx.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    (r'^$', views.handleRequest),
    
    url(r'^admin/', include(admin.site.urls)),
)
