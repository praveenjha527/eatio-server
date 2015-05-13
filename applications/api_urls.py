from django.conf.urls import patterns, include, url

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from applications.notifications_api import api as notification_views
from applications.accounts import api as account_api
from applications.review import api as review_api
from applications.restaurant import api as restaurant_api
from applications.globalprefs import views as global_settings
from applications.notifications_api import api as notification_api
from applications.accounts.api import FacebookLogin, PasswordResetRequestEmail, HelpTicketView , AccountPassword


router = DefaultRouter()

# Account routers
router.register(r'register', account_api.UserRegisterViewSet, base_name="register")
router.register(r'me', account_api.ProfileEditViewSet, base_name="edit")

# Review routers
router.register(r'review', review_api.ReviewViewSet)
router.register(r'accept-reject', review_api.AgreeDisagreeViewSet, base_name='accept_reject')

# Restaurant routers
router.register(r'restaurant', restaurant_api.RestaurantViewSet)
router.register(r'nearby-restaurant', restaurant_api.RestaurantNearbyViewSet, base_name="nearby")

# App Preference
router.register(r'preferences', global_settings.AppPreferencesView,base_name="configuration")

# Notification routers
router.register(r'notifications', notification_api.NotificationViewSet, base_name="notifications")

#search
router.register(r'search', review_api.ReviewSearchViewset, base_name='reviewsearch')

router.register(r'search', review_api.ReviewSearchViewset, base_name='reviewsearch')

urlpatterns = patterns('',
    url(r'^login/', views.obtain_auth_token),
    url(r'^change-password/$',AccountPassword.as_view(), name='api_account_password_change'),
    url(r'^', include(router.urls)),
    url(r'^facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^forgotpassword/$',PasswordResetRequestEmail.as_view(),name='password-reset'),
    url(r'^helpticket/$', HelpTicketView.as_view(), name = 'helpticket'),
    url(r'register_android_device/$',notification_views.RegisterAndroidDeviceTokenViewSet.as_view(),name='register-android-device'),
)

