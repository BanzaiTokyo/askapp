"""Add user created_by and modified_by foreign key refs to any model automatically.
   Almost entirely taken from https://github.com/Atomidata/django-audit-log/blob/master/audit_log/middleware.py"""
try:
    from django.utils.deprecation import MiddlewareMixin
    object = MiddlewareMixin
except:
    pass

from django.db.models import signals
from functools import partial
from django import http
from django.contrib import auth
from django.core import exceptions


class WhodidMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            if hasattr(request, 'user') and request.user.is_authenticated:
                user = request.user
            else:
                user = None

            mark_whodid = partial(self.mark_whodid, user)
            signals.pre_save.connect(mark_whodid,  dispatch_uid = (self.__class__, request,), weak = False)

    def process_response(self, request, response):
        signals.pre_save.disconnect(dispatch_uid =  (self.__class__, request,))
        return response

    def mark_whodid(self, user, sender, instance, **kwargs):
        if not hasattr(instance, 'modified_by_id'):
            instance.modified_by = user


class TokenMiddleware:
    """
    Middleware that authenticates against a token in the http authorization
    header.
    """
    get_response = None

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        if not self.get_response:
            return exceptions.ImproperlyConfigured(
                'Middleware called without proper initialization')

        self.process_request(request)

        return self.get_response(request)

    def process_request(self, request):
        auth_header = str(request.META.get('HTTP_AUTHORIZATION', '')).partition(' ')

        if auth_header[0].lower() != 'token':
            return None

        # If they specified an invalid token, let them know.
        if not auth_header[2]:
            return http.HttpResponseBadRequest("Improperly formatted token")

        user = auth.authenticate(token=auth_header[2])
        if user:
            request.user = user
