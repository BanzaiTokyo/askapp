from django import template
from allauth.socialaccount.models import SocialApp

register = template.Library()


@register.simple_tag
def provider_configured(provider):
    try:
        sapp = SocialApp.objects.get_current(provider)
        return sapp.client_id and sapp.secret
    except:
        return False
