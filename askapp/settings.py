import os
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

def get_env_variable(var_name, default_value=None):
    """Get the environment variable or return exception."""
    try:
        return os.environ[var_name] if default_value is None else os.getenv(var_name, default_value)
    except KeyError:
        error_msg = "Set the {} environment variable.".format(var_name)
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_env_variable('DJANGO_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INTERNAL_IPS = ['127.0.0.1', '::1']
ALLOWED_HOSTS = ['*', ]
SITE_ID = 1

# Application definition
INSTALLED_APPS = (
    'constance',
    'constance.backends.database',
    'askapp',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
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
    'memoize',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rules_light.middleware.Middleware',
    'pagination_bootstrap.middleware.PaginationMiddleware',
    'askapp.middleware.WhodidMiddleware',
    'askapp.middleware.TokenMiddleware',

)

ROOT_URLCONF = 'askapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/askapp/templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'askapp.context_processors.site_processor',
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
DB_HOST = get_env_variable('DB_HOST', 'localhost')
DB_NAME = get_env_variable('DB_NAME')
DB_USER = get_env_variable('DB_USER')
DB_PASSWORD = get_env_variable('DB_PASSWORD')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'OPTIONS': {'charset': 'utf8mb4'},
    }

}
# [END db_setup]

# [django-allauth] related parameters
# https://django-allauth.readthedocs.io/en/latest/configuration.html
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'askapp.backends.TokenBackend',
    #'allauth.account.auth_backends.AuthenticationBackend',
]
SOCIALACCOUNT_ADAPTER = "askapp.socialaccount.CustomSocialAccountAdapter"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_FORMS = {'signup': 'askapp.forms.RecaptchaRegistrationForm'}
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_LOGOUT_ON_GET = True
# [END django-allauth]

EMAIL = get_env_variable('EMAIL_ADDRESS')

# outgoing mail server settings
DEFAULT_FROM_EMAIL = EMAIL
EMAIL = EMAIL.split(' ')[-1].replace('<', '').replace('>', '')
SERVER_EMAIL = EMAIL
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

AUTH_USER_MODEL = 'auth.User'

FORCE_SCRIPT_NAME = os.getenv('PROJECT_PREFIX')
# the url where the user will be redirected after they log in
LOGIN_REDIRECT_URL = '/'

# List of domains that are not allowed to have email account on
# Confirmation email will silently fail to be sent
BLACKLISTED_DOMAINS = ['yopmail.com', ]

# STATIC_ROOT='static'
STATIC_ROOT = os.path.join(BASE_DIR, "askapp/static")

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'askapp/media')
MAX_IMAGE_SIZE = (640, 480)

AVATAR_SIZE = (100, 100)
DEFAULT_AVATAR_URL = STATIC_URL + 'images/avatar.png'

# number of threads per page
PAGINATION_DEFAULT_PAGINATION = 10
PAGINATION_DEFAULT_WINDOW = 2
PAGINATION_THREADS_PER_PROFILE = 3

# Markdown extensions
MARKDOWNX_MARKDOWN_EXTENSIONS = ['markdown.extensions.nl2br', ]
MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS = {}

# RECAPTCHA KEYS
RECAPTCHA_PRIVATE_KEY = get_env_variable('RECAPTCHA_PRIVATE_KEY', '')
RECAPTCHA_PUBLIC_KEY = get_env_variable('RECAPTCHA_PUBLIC_KEY', '')
RECAPTCHA_PROXY = 'http://127.0.0.1:8000'
# Google API key to get info from youtube videos
GOOGLE_API_KEY = get_env_variable('GOOGLE_API_KEY', '')
GOOGLE_ANALYTICS_ID = get_env_variable('GOOGLE_ANALYTICS_ID', '')

AUDIT_LOG_SIZE = 100
TECH_USER = 0  # specify user id to hide it from activity log

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_DATABASE_CACHE_BACKEND = 'default'
CONSTANCE_ADDITIONAL_FIELDS = {
    'image_field': ['django.forms.ImageField', {}]
}
CONSTANCE_CONFIG = {
    'SITE_NAME': ('', 'Site Name'),
    'SITE_LOGO': ('logo.png', 'Site logo', 'image_field'),
    'REGISTRATION_OPEN': (False, 'Is registration open?', bool),
    'NUM_DOMAIN_STATS': (50, 'number of rows in the table at the /domains page', int),
    'ABOUT_TEXT': ('', '"About" text')
}
