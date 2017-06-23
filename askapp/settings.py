"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from django.db.models import BooleanField, CharField

print("system=->", sys.path)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

def get_env_variable(var_name):
    """Get the environment variable or return exception."""
    print(os.environ[var_name])
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable.".format(var_name)
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_env_variable('DJANGO_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INTERNAL_IPS = ['127.0.0.1', '::1']

ALLOWED_HOSTS = ['*', ]

# Application definition
INSTALLED_APPS = (
    'siteprefs',
    'askapp',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'debug_toolbar',
    'snowpenguin.django.recaptcha2',
    'bootstrap3',
    'django_countries',
    'rules_light',
    'mptt',
    'pagination_bootstrap',
    'markdownx',
)

MIDDLEWARE_CLASSES = (
    'askapp.middleware.ForceDefaultLanguageMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'rules_light.middleware.Middleware',
    'pagination_bootstrap.middleware.PaginationMiddleware',
    'askapp.middleware.WhodidMiddleware',

)

ROOT_URLCONF = 'askapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(BASE_DIR) + '/askapp/templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.media',
                'askapp.context_processors.site_processor',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'askapp.wsgi.application'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/askapp_cache',
    }
}

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# [START db_setup]
# get database parameters from environment variables
DB_HOST = get_env_variable('DB_HOST')
DB_DATABASE = get_env_variable('DB_DATABASE')
DB_USER = get_env_variable('DB_USER')
DB_PASSWORD = get_env_variable('DB_PASSWORD')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_DATABASE,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
    }

}
# [END db_setup]

# [django-registration] related parameters
# https://django-registration.readthedocs.io/en/2.2/
ACCOUNT_ACTIVATION_DAYS = 7
# [END django-registration]

EMAIL = get_env_variable('EMAIL_ADDRESS')

# outgoing mail server settings
SERVER_EMAIL = EMAIL
DEFAULT_FROM_EMAIL = EMAIL
EMAIL_HOST_USER = EMAIL
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')
EMAIL_SUBJECT_PREFIX = '[Akihabara.Tokyo]'
EMAIL_HOST = get_env_variable('EMAIL_HOST')
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

TIME_ZONE = 'UTC'


USE_TZ = True

# =================== Internationalization
# inspired by the following tutorial:
# http://www.marinamele.com/taskbuster-django-tutorial/internationalization-localization-languages-time-zones

USE_I18N = True

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
    ('ru', _('Russian')),
)

YESNO = (
    (True, _("Yes")),
    (False, _("No"))
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'askapp/locale'),
)

# after adding new messages to templates run >>> python manage.py makemessages -l fr
# when the messages in the .po file are translated, run >>> python manage.py compilemessages -l fr
# =================== End Internationalization


# STATIC_ROOT='static'
STATIC_ROOT = os.path.join(BASE_DIR, "askapp/static")

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'auth.User'

# the url where the user will be redirected after they log in
LOGIN_REDIRECT_URL = '/'

# RECAPTCHA KEYS
RECAPTCHA_PRIVATE_KEY = get_env_variable('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_PUBLIC_KEY = get_env_variable('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PROXY = 'http://127.0.0.1:8000'

# List of domains that are not allowed to have email account on
# Confirmation email will silently fail to be sent
BLACKLISTED_DOMAINS = ['yopmail1.com', ]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'askapp/media')

AVATAR_SIZE = (100, 100)
DEFAULT_AVATAR_URL = STATIC_URL + 'images/avatar.png'

# number of threads per page
PAGINATION_DEFAULT_PAGINATION = 10
PAGINATION_DEFAULT_WINDOW = 2
PAGINATION_THREADS_PER_PROFILE = 3

# setting used by Django "sites" framework
SITE_NAME = 'Akihabara'

# Markdown extensions
MARKDOWNX_MARKDOWN_EXTENSIONS = ['markdown.extensions.nl2br', ]
MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS = {}

REGISTRATION_OPEN = False
GOOGLE_ANALYTICS_ID = ''

# number of rows in the table at the /domains page
NUM_DOMAIN_STATS = 3

UPVOTES_PER_DAY = 3

from siteprefs.toolbox import patch_locals, register_prefs, pref, pref_group
patch_locals()  # required by django-siteprefs manual
register_prefs(  # Now we register our settings to make them available as siteprefs.
        # And finally we register a non-static setting with extended meta for Admin.
        pref(SITE_NAME, verbose_name=_('Site Name'), static=False),
        pref(RECAPTCHA_PUBLIC_KEY, verbose_name=_('ReCAPTCHA Public Key'), static=False),
        pref(RECAPTCHA_PRIVATE_KEY, verbose_name=_('ReCAPTCHA Private Key'), static=False),
        pref(LANGUAGE_CODE, verbose_name=_('Site Language'), static=False, field=CharField(choices=LANGUAGES, max_length=2)),
        pref(REGISTRATION_OPEN, verbose_name=_('Is registration open?'), static=False, field=BooleanField(choices=YESNO)),
        pref(GOOGLE_ANALYTICS_ID, verbose_name=_('Google Analytics ID'), static=False, field=CharField(max_length=15, blank=True, null=True)),
        pref(EMAIL_SUBJECT_PREFIX, verbose_name=_('Email subject prefix'), static=False),
        pref(NUM_DOMAIN_STATS, verbose_name=_('/domains page length'), static=False),
        pref(UPVOTES_PER_DAY, verbose_name=_('Number of upvotes per day'), static=False),
    )
# Add string methods to
from siteprefs.utils import PrefProxy, PatchedLocal
def prefproxy_find(self, sub, start=None, end=None):
    return str(self).find(sub, start, end)
def prefproxy_lower(self):
    return str(self).lower()
def prefproxy_getitem(self, key):
    return str(self).__getitem__(key)
def prefproxy_split(self, sep=None, maxsplit=-1):
    return str(self).split(sep, maxsplit)
PrefProxy.find = prefproxy_find
PrefProxy.__getitem__ = prefproxy_getitem
PrefProxy.lower = prefproxy_lower
PrefProxy.split = prefproxy_split
def patchedlocal_iter(self):
    return iter(self.val)
PatchedLocal.__iter__ = patchedlocal_iter
