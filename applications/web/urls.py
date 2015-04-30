from django.conf.urls import patterns, url
from applications.web.views import PasswordResetView
from applications.web.views import ContactUs

urlpatterns = patterns('',
        url(r'password_reset/(?P<user_id>[0-9a-zA-Z]{1,13})-(?P<token>.+)/$',
        PasswordResetView.as_view(),
        name = 'password_reset'
    ),
        url(r'contactus/$', ContactUs.as_view(),
    ),
        )