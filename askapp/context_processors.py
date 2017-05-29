from .settings import SITE_NAME

def site_processor(request):
    return { 'site_name': SITE_NAME }