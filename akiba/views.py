from django.shortcuts import render
from django.views.generic import View
from registration.views import RegistrationView
from akiba.forms import RecaptchaRegistrationForm


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

    def register(self, form):
        """
        Implement user-registration logic here. Access to both the
        request and the registration form is available here.

        """
        raise NotImplementedError
