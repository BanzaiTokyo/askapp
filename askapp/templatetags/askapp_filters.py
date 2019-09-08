import markdown
from askapp import settings
from django import template
from django.utils.safestring import mark_safe
import re
from django.urls import reverse

register = template.Library()

@register.filter(is_safe=True)
def markdownify(content):
    s = markdown.markdown(
        content,
        extensions=settings.MARKDOWNX_MARKDOWN_EXTENSIONS,
        extension_configs=settings.MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS
    )
    return mark_safe(s)

@register.filter(is_safe=True)
def markdownify_noimages(content):
    s = re.sub(r'\!\[\]\([\/\w\-\.]+\)', '', content)
    return markdownify(s)

@register.simple_tag(takes_context=True)
def url_active(context, viewname):
    request = context['request']
    current_path = request.path
    compare_path = reverse(viewname)
    if current_path == compare_path:
        return 'active'
    else:
        return ''

@register.filter
def avatar_url(user):
    return (user.profile.avatar.url if hasattr(user, 'profile') else '') or settings.DEFAULT_AVATAR_URL
