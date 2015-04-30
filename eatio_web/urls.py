from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from applications.web.views import HomePageView

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^eatio-admin/', include(admin.site.urls)),
    url(r'^api/v1/', include('applications.api_urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^web/', include('applications.web.urls')),
    url(r'^acra/', include("applications.acra.urls")),
)

urlpatterns += patterns('',
        (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.MEDIA_ROOT,}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns

urlpatterns += staticfiles_urlpatterns()
