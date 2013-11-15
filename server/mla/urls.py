from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = patterns('',
                       url(r'^$', RedirectView.as_view(url="/static/index.html")),
                       url(r'^annotation/?$', views.AnnotationList.as_view(), name='api-annotation-list'),
                       url(r'^annotation/(?P<pk>[0-9]+)/?$', views.AnnotationDetail.as_view(), name='api-annotation-detail'),
                       )
