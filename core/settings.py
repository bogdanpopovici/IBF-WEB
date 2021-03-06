import os, subprocess, string
from django.db.utils import OperationalError
from django.db import connections

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cex*3hzvkh18k7l3m+y*(5lqq-v^%_xx#*%k)nuv*pwtulkyya'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'paypal.standard',
    'paypal.pro',
    'paypal.standard.ipn',
    'public',
    'paypalapp',
    'haystack',
    'search_engine',
    'core',
    'android_module',
    'staticpages',
    'ibfAPI',
    'mathfilters',
    'analytical',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.Facebook2OAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'public.pipeline.require_email',
    'social.pipeline.mail.mail_validation',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.debug.debug',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'public.pipeline.user_details',
    'social.pipeline.debug.debug'
)

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'core.wsgi.application'


#====================Database setup========================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''
if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'ibf-web',
            'USER': 'user',
            'PASSWORD': 'password', 
        }
    }

'''
#=============SearchEngine Setup=================

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL' : 'search-ibf-es-tdw2x7ovuds4tqycwd7f336axe.us-west-2.es.amazonaws.com:80',
        'INDEX_NAME': 'haystack',
    },
}


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = './static'
MEDIA_ROOT = './media' 
MEDIA_URL = '/media/'
LOGIN_URL = '/'

#==========Email Setup using Gmail platform==============

EMAIL_HOST = 'olympus.krystal.co.uk'
EMAIL_HOST_USER = 'hello@ivebeenfound.com'
EMAIL_HOST_PASSWORD = 'E-nddubQDXb6'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'hello@ivebeenfound.com'

#==========Custom User Model=============================

AUTH_USER_MODEL = 'core.CustomUser'

#==========Social Integration Settings====================

SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_TWITTER_KEY = 'CvelfR7ZHWnc54xYDBtjl3UYj'
SOCIAL_AUTH_TWITTER_SECRET = 'UnO1ZhDYvgQQ10jMNARVOsOcwukgG0QVb6YkNbtqxVuIa7rOEg'

SOCIAL_AUTH_FACEBOOK_KEY = '882465798506028'
SOCIAL_AUTH_FACEBOOK_SECRET = '838dd6875ea335f5a489fbca9ff8a077'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

#==========paypal integration settings======================

PAYPAL_TEST = True
PAYPAL_WPP_USER = "pbp1g12_api1.soton.ac.uk"
PAYPAL_WPP_PASSWORD = "24U5CU57CDE224FZ"
PAYPAL_WPP_SIGNATURE = "AFcWxV21C7fd0v3bYYYRCpSSRl31AgaCQ0HaFjkigPaC.eZZZqsGeK6I"
PAYPAL_RECEIVER_EMAIL = "bogdan_gem@yahoo.com"

#==========google analitycs integration======================
GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-74499271-1'