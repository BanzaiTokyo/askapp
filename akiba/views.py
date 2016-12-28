from django.shortcuts import render, redirect
from django.views.generic import View
from registration.backends.hmac.views import RegistrationView
from django.conf import settings
from akiba import forms, models
from akiba.settings import BLACKLISTED_DOMAINS
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy
import rules_light
import auth_rules
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


class ProfileView(DetailView):
    model = models.User
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        return context


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


class ThreadView(DetailView):
    model = models.Thread
    template_name = 'thread.html'

    def get_context_data(self, **kwargs):
        context = super(ThreadView, self).get_context_data(**kwargs)
        return context


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


class NewThreadView(LoginRequiredMixin, CreateView):
    form_class = forms.NewThreadForm
    template_name = 'new_thread.html'

    def get_success_url(self):
        return reverse_lazy('thread', args=(self.object.id,))


@rules_light.class_decorator('akiba.thread.update')
class EditThreadView(LoginRequiredMixin, UpdateView):
    form_class = forms.EditThreadForm
    model = models.Thread
    template_name = 'new_thread.html'

    def get_context_data(self, **kwargs):
        context = super(EditThreadView, self).get_context_data(**kwargs)
        context['hide_type'] = True
        return context

    def get_success_url(self):
        return reverse_lazy('thread', args=(self.object.id,))


class ReplyMixin(LoginRequiredMixin, CreateView):
    """
    Common class for inline and standalone comment form
    """
    form_class = forms.ReplyForm
    model = models.Post

    def get_form(self, form_class=None):
        if not hasattr(self, 'thread'):
            thread_id = self.kwargs.get('thread_id')
            self.thread = models.Thread.objects.get(pk=thread_id)
        rules_light.require(self.request.user, 'akiba.post.create', self.thread)
        return super(ReplyMixin, self).get_form(form_class)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.thread = self.thread
        return super(ReplyMixin, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('thread', args=(self.kwargs.get('thread_id'),))


class ReplyThreadView(ReplyMixin):
    """
    Inline comment handler
    """
    template_name = 'index.html'

    def form_invalid(self, form):
        return redirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        return redirect(self.get_success_url())


class ReplyCommentView(ReplyMixin):
    """
    Standalone comment handler
    """
    template_name = 'comment.html'

    def get_form(self, form_class=None):
        post_id = self.kwargs.get('post_id')
        self.post = models.Post.objects.get(pk=post_id)
        self.kwargs['thread_id'] = self.post.thread.id  # for get_success_url()
        return super(ReplyCommentView, self).get_form(form_class)

    def get_context_data(self, **kwargs):
        context = {'object': self.post}
        context.update(kwargs)
        return super(ReplyCommentView, self).get_context_data(**context)

    def form_valid(self, form):
        form.instance.parent = self.post
        return super(ReplyCommentView, self).form_valid(form)


class DeleteCommentView(LoginRequiredMixin, View):
    """
    Actually this is not a view, but just a request handler
    """
    def get(self, request, *args, **kwargs):
        post = models.Post.objects.get(pk=kwargs['post_id'])
        rules_light.require(self.request.user, 'akiba.post.delete', post)
        post.deleted = True
        post.save()
        return redirect(reverse_lazy('thread', args=(post.thread.id, )))


class TagView(DetailView):
    """
    Display threads by tag
    """
    template_name = 'index.html'
    model = models.Tag
