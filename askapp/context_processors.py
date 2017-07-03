from .settings import SITE_NAME, ABOUT_TEXT

def site_processor(request):
    return { 'site_name': SITE_NAME, 'about_text': ABOUT_TEXT }