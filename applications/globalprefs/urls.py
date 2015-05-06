from django.conf.urls import patterns, url
from applications.globalprefs.views import PrivacyPolicyView
# from applications.globalprefs.views import

urlpatterns = patterns('',
        url(r'^privacypolicy/$',PrivacyPolicyView.as_view(), name = 'privacypolicy'
    ),

        )