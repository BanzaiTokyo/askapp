from .settings import SITE_NAME, ABOUT_TEXT, GOOGLE_ANALYTICS_ID

def site_processor(request):
    return { 'site_name': SITE_NAME, 'about_text': ABOUT_TEXT, 'google_analytics_id': str(GOOGLE_ANALYTICS_ID) }