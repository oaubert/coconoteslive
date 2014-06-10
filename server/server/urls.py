from django.views.generic import RedirectView
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', RedirectView.as_view(url="/mla/", permanent=False)),
                       url(r'^mla/', include('mla.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       )
