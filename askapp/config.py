from django.apps import AppConfig
from django.db.models import BooleanField, CharField
from siteprefs.toolbox import preferences

from .settings import *


class AskappConfig(AppConfig):
    name = 'askapp'


with preferences() as prefs:
    prefs(
        prefs.one(SITE_NAME, verbose_name='Site Name', static=False),
        prefs.one(RECAPTCHA_PUBLIC_KEY, verbose_name='ReCAPTCHA Public Key', static=False),
        prefs.one(RECAPTCHA_PRIVATE_KEY, verbose_name='ReCAPTCHA Private Key', static=False),
        prefs.one(REGISTRATION_OPEN, verbose_name='Is registration open?', static=False,
                  field=BooleanField(choices=((True, "Yes"), (False, "No")))),
        prefs.one(GOOGLE_ANALYTICS_ID, verbose_name='Google Analytics ID', static=False,
                  field=CharField(max_length=15, blank=True, null=True)),
        prefs.one(EMAIL_SUBJECT_PREFIX, verbose_name='Email subject prefix', static=False),
        prefs.one(NUM_DOMAIN_STATS, verbose_name='/domains page length', static=False),
        prefs.one(UPVOTES_PER_DAY, verbose_name='Number of upvotes per day', static=False),
        prefs.one(ABOUT_TEXT, verbose_name='"About" text', static=False),
    )
