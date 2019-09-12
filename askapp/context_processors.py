import os
from django.conf import settings as s


def site_processor(request):
    site_logo = getattr(s, 'SITE_LOGO')
    if not os.path.isfile(os.path.join(s.STATIC_ROOT, site_logo)):
        site_logo = None
    result = {
        'site_name': getattr(s, 'SITE_NAME', ''),
        'site_logo': site_logo,
        'about_text': getattr(s, 'ABOUT_TEXT', ''),
        'google_analytics_id': getattr(s, 'GOOGLE_ANALYTICS_ID', '')
    }
    return result
