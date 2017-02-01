import markdown
from askapp.settings import MARKDOWNX_MARKDOWN_EXTENSIONS, MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS
from django import template
from django.utils.safestring import mark_safe
import re
from math import ceil, floor

register = template.Library()

@register.filter(is_safe=True)
def markdownify(content):
    s = markdown.markdown(content, extensions=MARKDOWNX_MARKDOWN_EXTENSIONS, extension_configs=MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS)
    return mark_safe(s)

@register.filter(is_safe=True)
def markdownify_noimages(content):
    s = re.sub(r'\!\[\]\([\/\w\-\.]+\)', '', content)
    return markdownify(s)

@register.filter
def farfrom(value, arg):
    "value is for-loop index, arg is list"
    n = float(value) - len(arg)/2.0
    n = int(ceil(n) if n > 0 else floor(n))
    return n-1 if n > 0 else -n
