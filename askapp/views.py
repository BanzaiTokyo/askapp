from django.shortcuts import render, redirect
from django.views.generic import View
from registration.backends.hmac.views import RegistrationView
from django.conf import settings
from askapp import forms, models
from askapp.settings import BLACKLISTED_DOMAINS
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy
from django.db.models import ObjectDoesNotExist
from django.http import Http404

import rules_light
import askapp.auth_rules
import logging


class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_active:
            return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


class HomeView(View):
    def get_threads(self):
        return models.Thread.objects.all().order_by('-score')

    def get(self, request, *args, **kwargs):
        context = {
            'threads': self.get_threads(),
            'tags': models.Tag.objects.all(),
            'users': models.User.objects.filter(is_active=True).order_by('-date_joined')[:5]
        }
        return render(request, 'index.html', context)


class RecentThreadsView(HomeView):
    def get_threads(self):
        return models.Thread.objects.all().order_by('-created')


class ProfileView(DetailView):
    model = models.User
    template_name = 'profile.html'

    def get_context_object_name(self, obj):
        return 'object'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['threads'] = models.Thread.objects.filter(user=self.object).order_by('-created')
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


@rules_light.class_decorator('askapp.profile.update')
class AdminProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = forms.ProfileForm
    template_name = 'profile_edit.html'
    model = models.Profile

    def get_context_data(self, **kwargs):
        context = super(AdminProfileEditView, self).get_context_data(**kwargs)
        context['admin_view'] = True
        return context

    def get_object(self, queryset=None):
        user = models.User.objects.get(id=self.kwargs['pk'])
        try:
            profile = user.profile
        except:
            return models.Profile.objects.model(user=user)
        return profile

    def post(self, request, *args, **kwargs):
        if 'block_user' in request._post:
            user = models.User.objects.get(id=self.kwargs['pk'])
            user.is_active = False
            user.save(update_fields={'is_active': False})
            self.object = user.profile
            return redirect(self.get_success_url())
        else:
            return super(AdminProfileEditView, self).post(self, request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('profile', args=(self.object.user.id,))


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


class AskappRegistrationView(RegistrationView):
    form_class = forms.RecaptchaRegistrationForm
    template_name = 'registration_form.html'

    @staticmethod
    def is_email_blacklisted(email):
        return any([email.lower().endswith('@'+d) for d in BLACKLISTED_DOMAINS])

    def send_activation_email(self, user):
        if self.is_email_blacklisted(user.email):
            logging.debug('blacklisted email %s', user.email)
        else:
            super(AskappRegistrationView, self).send_activation_email(user)


class NewThreadView(LoginRequiredMixin, CreateView):
    form_class = forms.NewThreadForm
    template_name = 'new_thread.html'

    def get_success_url(self):
        return reverse_lazy('thread', args=(self.object.id,))


@rules_light.class_decorator('askapp.thread.update')
class EditThreadView(LoginRequiredMixin, UpdateView):
    form_class = forms.EditThreadForm
    model = models.Thread
    template_name = 'new_thread.html'

    def get_context_data(self, **kwargs):
        context = super(EditThreadView, self).get_context_data(**kwargs)
        context['hide_type'] = True
        context['hide_link'] = self.object.thread_type != 'LL'
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
        rules_light.require(self.request.user, 'askapp.post.create', self.thread)
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
        rules_light.require(request.user, 'askapp.post.delete', post)
        post.deleted = True
        post.save()
        return redirect(reverse_lazy('thread', args=(post.thread.id, )))


class TagView(HomeView):
    """
    Display threads by tag
    """
    def get_threads(self):
        try:
            tag = models.Tag.objects.get(slug=self.kwargs['slug'])
        except ObjectDoesNotExist:
            raise Http404
        return tag.thread_set.order_by('-created')


class ThreadLikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        thread = models.Thread.objects.get(pk=kwargs['thread_id'])
        rules_light.require(request.user, 'askapp.threadlike.create', thread)
        models.ThreadLike.vote(thread, request.user, kwargs['verb'])
        return redirect(request.META.get('HTTP_REFERER', reverse_lazy('thread', args=(thread.id))))


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post = models.Post.objects.get(pk=kwargs['post_id'])
        rules_light.require(request.user, 'askapp.postlike.create', post)
        models.PostLike.vote(post, request.user, kwargs['verb'])
        return redirect(request.META.get('HTTP_REFERER', reverse_lazy('thread', args=(post.thread.id))))
