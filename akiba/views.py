from django.shortcuts import render, redirect
from django.views.generic import View
from registration.backends.hmac.views import RegistrationView
from django.conf import settings
from akiba import forms, models
from akiba.settings import BLACKLISTED_DOMAINS
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
import logging


class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_active:
            return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


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


class ProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = forms.ProfileForm
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('profile_edit')

    def get_object(self, queryset=None):
        try:
            profile = self.request.user.profile
        except:
            return models.Profile.objects.model(user=self.request.user)
        return profile


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
    form_class = forms.RecaptchaRegistrationForm
    template_name = 'registration_form.html'

    @staticmethod
    def is_email_blacklisted(email):
        return any([email.lower().endswith('@'+d) for d in BLACKLISTED_DOMAINS])

    def send_activation_email(self, user):
        if self.is_email_blacklisted(user.email):
            logging.debug('blacklisted email %s', user.email)
        else:
            super(AkibaRegistrationView, self).send_activation_email(user)
