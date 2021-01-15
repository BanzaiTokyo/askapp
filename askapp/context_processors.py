import os
from django.conf import settings as s
from constance import config


def site_processor(request):
    site_logo = s.MEDIA_URL + config.SITE_LOGO if config.SITE_LOGO else None
    result = {
        'site_name': config.SITE_NAME,
        'site_logo': site_logo,
        'about_text': config.ABOUT_TEXT,
        'google_analytics_id': s.GOOGLE_ANALYTICS_ID
    }
    return result
