import os
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = patterns('',
                       url(r'^$', views.root, name='root'),
                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.dirname(os.path.normpath(__file__)) + '/static' }),
                       url(r'^(?P<group>\w+)/annotation/$', views.AnnotationList.as_view(), name='api-annotation-list'),
                       url(r'^(?P<group>\w+)/annotation/(?P<pk>[0-9]+)/$', views.AnnotationDetail.as_view(), name='api-annotation-detail'),
                       url(r'^(?P<group>\w+)/(?P<shortcut>.*)$', views.group_view, name='group-view'),
                       )
