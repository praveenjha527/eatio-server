"""
Django settings for eatio_web project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from logentries import LogentriesHandler
import logging


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.path.pardir))
SUPER_DIR = os.path.abspath(os.path.join(PROJECT_DIR, os.path.pardir))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4=&!329zsw^@&-!z&6!$3e$jv=+w_p6rqn9_xnjq3bn&w(nu48'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = (
    'djangocms_admin_style',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',


    # 3rd party apps
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'notifications',
    'mailer',
    'rest_framework_swagger',
    'push_notifications',
    'robots',
    'ckeditor',

    # preferences for the app as a whole
    'solo',

    # Custom Apps
    'applications.accounts',
    'applications.restaurant',
    'applications.review',
    'applications.globalprefs',
    'applications.web',
    'acra',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',

)

ROOT_URLCONF = 'eatio_web.urls'

WSGI_APPLICATION = 'eatio_web.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

STATICFILES_DIRS = (os.path.join(PROJECT_DIR, 'staticfiles'), )

# media

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

AUTH_USER_MODEL = 'accounts.User'

CKEDITOR_UPLOAD_PATH = "uploads/"

# template directories
TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR,  'templates'),
)

# Rest framework
REST_FRAMEWORK = {
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'limit',
    'MAX_PAGINATE_BY': 100,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

SITE_ID = 1


SWAGGER_SETTINGS = {
    "exclude_namespaces": [],  # List URL namespaces to ignore
    "api_version": '0.1',  # Specify your API's version
    "api_path": "/",  # Specify the path to your API not a root level
    "enabled_methods": [  # Specify which methods to enable in Swagger UI
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
    "api_key": '',  # An API key
    "is_authenticated": False,  # Set to True to enforce user authentication,
    "is_superuser": False,  # Set to True to enforce admin only access
                            # todo: set it to True before deploy for security
}

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "allauth.socialaccount.context_processors.socialaccount",
)

REVIEWS_HOURS_COUNT = 80  # expiry hours
REVIEWS_FETCH_DISTANCE = 3  # minimum distance to get the list of reviews from the centre circular point
RESTAURANT_DEFAULT_IMAGE = ""  # Default Images

##########      OTHER SETTINGS TO BE PUT IN GLOBALPREFS LATER           ##########

SIGNUP_BONUS = 100
GENERATE_SIGNUP_BONUS_AND_NOTIFY = True
REFERRAL_POINTS = 50

# Foursquare API details
FOURSQUARE_API = "https://api.foursquare.com"
FOURSQUARE_VENUE_DETAIL_API_URL = "%s/v2/venues/" % FOURSQUARE_API
FOURSQUARE_VENUE_SEARCH_API_URL = "%s/v2/venues/search" % FOURSQUARE_API
FOURSQUARE_CLIENT_ID = "SWODPYUXPE4PVBZDF3R1DXLQFIT4QSSEBBZMYTPCDBHXRFQD"
FOURSQUARE_CLIENT_SECRET = "QY4LPUTYFB5OGOYJA4352SOK54NA35QUJHO3XLU2GKKBG0UQ"
FOURSQUARE_CATEGORY_ID = "4d4b7105d754a06374d81259"
FOURSQUARE_PHOTO_SIZE = "300x300"
FOURSQUARE_INTENT = "browse"
FOURSQUARE_RADIUS = 1000

############        TIMELOG         ####################


# Email setup for password recovery
EMAIL_BACKEND = "mailer.backend.DbBackend"

# hello eatio email configurations
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_POST = 465
EMAIL_HOST_USER = 'hello_eatio'
DEFAULT_FROM_EMAIL = 'Eatio <hello@eatio.co>'
EMAIL_HOST_PASSWORD = 'bS656Gqp'
EMAIL_USE_TLS = True

SERVER_EMAIL = EMAIL_HOST_USER

GOOGLE_PLAY_APP_LINK = ""


# Push Notification


PUSH_NOTIFICATIONS_SETTINGS = {
    "GCM_API_KEY": "AIzaSyDoGTXmirHWbBP1nmUD6f0Yv1uADT2VatE",
}

#CK editor Configuration


CKEDITOR_CONFIGS = {
   'default': {
       'toolbar': 'full',
       'height': 300,
       'width': 600,
   },
}

ACCOUNT_ADAPTER = 'applications.utils.adapters.MessageFreeAdapter'
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'METHOD': 'oauth2'  # instead of 'oauth2'
    }
}