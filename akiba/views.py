from django.shortcuts import render
from django.views.generic import View
from registration.backends.hmac.views import RegistrationView
from akiba.forms import RecaptchaRegistrationForm
from akiba.settings import BLACKLISTED_DOMAINS
import logging


class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'key1': "value",
        }
        return render(request, 'index.html', context)


class NewRegisterView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'key1': "value",
        }
        return render(request, 'new-registration.html', context)

class ThankyouView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'key1': "value",
        }
        return render(request, 'content.html', context)

class NewLoginView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'key1': "value",
        }
        return render(request, 'new-login.html', context)

class ProfileEditView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'key1': "value",
        }
        return render(request, 'profile_edit.html', context)

class ThreadView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'key1': "value",
        }
        return render(request, 'thread.html', context)

class QuestionView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'key1': "value",
        }
        return render(request, 'question.html', context)


class CommentView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'key1': "value",
        }
        return render(request, 'comment.html', context)



class AkibaRegistrationView(RegistrationView):
    form_class = RecaptchaRegistrationForm
    template_name = 'registration_form.html'

    @staticmethod
    def is_email_blacklisted(email):
        return any([email.lower().endswith('@'+d) for d in BLACKLISTED_DOMAINS])

    def send_activation_email(self, user):
        if self.is_email_blacklisted(user.email):
            logging.debug('blacklisted email %s', user.email)
        else:
            super(AkibaRegistrationView, self).send_activation_email(user)
