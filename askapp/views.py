from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from registration.backends.hmac.views import RegistrationView
from django.conf import settings
from askapp import forms, models
from askapp.score_calcuator import calculate_scores
from askapp.settings import BLACKLISTED_DOMAINS, REGISTRATION_OPEN, SITE_NAME
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy
from django.db.models import ObjectDoesNotExist
from django.http import Http404
from django.template.defaultfilters import slugify
from django.core.urlresolvers import resolve
from django.db.models import Q, Count, Avg

from datetime import datetime, timedelta

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
        return models.Thread.objects.filter( Q(sticky__isnull=True) | Q(sticky__lt=datetime.now()), deleted=False).order_by('-score')[:10]

    def get_sticky(self):
        return models.Thread.objects.filter(deleted=False, sticky__isnull=False, sticky__gte=datetime.now())

    def get(self, request, *args, **kwargs):
        calculate_scores()
        context = {
            'home_page': resolve(request.path_info).url_name == 'index'
        }
        context.update({
            'threads': self.get_threads(),
            'sticky': self.get_sticky() if context['home_page'] or getattr(self.request, 'page') == 1 else [],
            'tags': models.Tag.objects.all(),
            'users': models.User.objects.filter(is_active=True).order_by('-date_joined')[:5],
        })
        return render(request, 'index.html', context)


class RecentThreadsView(HomeView):
    def get_threads(self):
        if getattr(self.request, 'page') == 1:
            return models.Thread.objects.filter( Q(sticky__isnull=True) | Q(sticky__lt=datetime.now()), deleted=False).order_by('-created')
        else:
            return models.Thread.objects.filter(deleted=False).order_by('-created')


class FavoriteThreadsView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'home_page': False,
            'threads': self.request.user.profile.favorite_threads,
        }
        return render(request, 'favorites.html', context)


class ProfileView(DetailView):
    model = models.User
    template_name = 'profile.html'

    def get_context_object_name(self, obj):
        return 'object'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['threads'] = models.Thread.objects.filter(user=self.object, deleted=False).order_by('-created')
        context['per_page'] = settings.PAGINATION_THREADS_PER_PROFILE
        context['admin_view'] = self.request.user.is_staff
        context['favorites'] = self.request.user.profile.favorite_threads
        return context


# class NewRegisterView(View):
#     def get(self, request, *args, **kwargs):
#         context = {
#             'key1': "value",
#         }
#         return render(request, 'new-registration.html', context)
#
# class ThankyouView(View):
#     def get(self, request, *args, **kwargs):
#         context = {
#             'key1': "value",
#         }
#         return render(request, 'content.html', context)

# class NewLoginView(View):
#     def get(self, request, *args, **kwargs):
#         context = {
#             'key1': "value",
#         }
#         return render(request, 'new-login.html', context)


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

    def get_initial(self):
        params = super(AdminProfileEditView, self).get_initial()
        params['is_active'] = self.object.user.is_active
        return params

    def get_context_data(self, **kwargs):
        context = super(AdminProfileEditView, self).get_context_data(**kwargs)
        context['admin_view'] = True
        return context

    def get_object(self, queryset=None):
        user = get_object_or_404(models.User, id=self.kwargs['pk'])
        try:
            profile = user.profile
        except:
            return models.Profile.objects.model(user=user)
        return profile

    def post(self, request, *args, **kwargs):
        if 'block_user' in request._post:
            user = get_object_or_404(models.User, id=self.kwargs['pk'])
            user.is_active = False
            user.save(update_fields={'is_active': False})
            self.object = user.profile
            return redirect(self.get_success_url())
        else:
            return super(AdminProfileEditView, self).post(self, request, *args, **kwargs)

    def get_success_url(self):
        # profile saved, work with is_active
        self.object.user.is_active = self.request.POST.get('is_active', 'off') == 'on'
        self.object.user.save(update_fields=['is_active'])
        return reverse_lazy('profile', args=(self.object.user.id,))


class ThreadView(DetailView):
    model = models.Thread

    def get_template_names(self):
        return 'thread_question.html' if self.object.thread_type == self.object.QUESTION else 'thread.html'

    def get_context_data(self, **kwargs):
        context = super(ThreadView, self).get_context_data(**kwargs)
        print(context['object'].answers)
        return context


# class QuestionView(View):
#     def get(self, request, *args, **kwargs):
#         context = {
#             'key1': "value",
#         }
#         return render(request, 'question.html', context)


class CommentView(CreateView):
    model = models.Post
    template_name = 'comment.html'

    def get_context_data(self, **kwargs):
        context = super(CommentView, self).get_context_data(**kwargs)
        return context


class AskappRegistrationView(RegistrationView):
    form_class = forms.RecaptchaRegistrationForm
    template_name = 'registration_form.html'

    def registration_allowed(self):
        """
        This method returns proper settings.REGISTRATION_OPEN value when used with django-siteprefs
        """
        return REGISTRATION_OPEN.get_value()

    @staticmethod
    def is_email_blacklisted(email):
        return any([email.lower().endswith('@'+d) for d in BLACKLISTED_DOMAINS])

    def get_email_context(self, activation_key):
        result = super(AskappRegistrationView, self).get_email_context(activation_key)
        class objectview(object):
            def __init__(self, d):
                self.__dict__ = d
        result['site'] = objectview({'domain': self.request.get_host(), 'name': SITE_NAME})
        return result

    def send_activation_email(self, user):
        if self.is_email_blacklisted(user.email):
            logging.debug('blacklisted email %s', user.email)
        else:
            super(AskappRegistrationView, self).send_activation_email(user)


class ThreadMixin(object):
    form_class = forms.ThreadForm
    template_name = 'thread_edit.html'
    def get_form_kwargs(self):
        kwargs = super(ThreadMixin, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('thread', args=(self.object.id, slugify(self.object.title)))


class NewThreadView(LoginRequiredMixin, ThreadMixin, CreateView):
    pass


@rules_light.class_decorator('askapp.thread.update')
class EditThreadView(LoginRequiredMixin, ThreadMixin, UpdateView):
    model = models.Thread

    def get_context_data(self, **kwargs):
        context = super(EditThreadView, self).get_context_data(**kwargs)
        context['admin_view'] = self.request.user.is_staff
        return context


@rules_light.class_decorator('askapp.thread.delete')
class DeleteThreadView(LoginRequiredMixin, UpdateView):
    success_url = reverse_lazy('index')
    model = models.Thread
    fields = ['deleted']
    template_name = 'thread_delete.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.deleted = True
        instance.delete_reason = self.request.POST.get('reason', '')
        return super(DeleteThreadView, self).form_valid(form)


class LockThreadView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        thread = get_object_or_404(models.Thread, pk=kwargs['thread_id'])
        rules_light.require(request.user, 'askapp.thread.update', thread)
        thread.closed = not thread.closed
        thread.save()
        return redirect(reverse_lazy('thread', args=(thread.id, slugify(thread.title))))


class ReplyMixin(CreateView):
    """
    Common class for inline and standalone comment form
    """
    form_class = forms.ReplyForm
    model = models.Post

    def get_form(self, form_class=None):
        if not hasattr(self, 'thread'):
            thread_id = self.kwargs.get('thread_id')
            self.thread = get_object_or_404(models.Thread, pk=thread_id)
        if self.request.method == 'POST':
            rules_light.require(self.request.user, 'askapp.post.create', self.thread)
            if hasattr(self, 'post_object'):
                rules_light.require(self.request.user, 'askapp.post.reply', self.post_object)
        return super(ReplyMixin, self).get_form(form_class)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.thread = self.thread
        return super(ReplyMixin, self).form_valid(form)

    def get_success_url(self):
        if not self.kwargs.get('slug'):
            thread = models.Thread.objects.get(pk=self.kwargs.get('thread_id'))
            self.kwargs['slug'] = slugify(thread.title)
        return reverse_lazy('thread', args=(self.kwargs.get('thread_id'), self.kwargs.get('slug')))


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
        self.post_object = get_object_or_404(models.Post, pk=post_id)
        self.kwargs['thread_id'] = self.post_object.thread.id  # for get_success_url()
        return super(ReplyCommentView, self).get_form(form_class)

    def get_context_data(self, **kwargs):
        context = {'object': self.post_object}
        context.update(kwargs)
        return super(ReplyCommentView, self).get_context_data(**context)

    def form_valid(self, form):
        form.instance.parent = self.post_object
        return super(ReplyCommentView, self).form_valid(form)


class DeleteCommentView(LoginRequiredMixin, View):
    """
    Actually this is not a view, but just a request handler
    """
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(models.Post, pk=kwargs['post_id'])
        rules_light.require(request.user, 'askapp.post.delete', post)
        post.deleted = True
        post.save()
        return redirect(reverse_lazy('thread', args=(post.thread.id, slugify(post.thread.title))))


class DeleteCommentTreeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        rules_light.require(request.user, 'askapp.post.delete_all', None)
        post = get_object_or_404(models.Post, pk=kwargs['post_id'])
        post.get_descendants(include_self=True).update(deleted=1)
        return redirect(reverse_lazy('thread', args=(post.thread.id, slugify(post.thread.title))))


class TagView(HomeView):
    """
    Display threads by tag
    """
    def get_threads(self):
        try:
            tag = get_object_or_404(models.Tag, slug=self.kwargs['slug'])
        except ObjectDoesNotExist:
            raise Http404
        return tag.thread_set.order_by('-created')


class ThreadLikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        thread = get_object_or_404(models.Thread, pk=kwargs['thread_id'])
        rules_light.require(request.user, 'askapp.threadlike.%s' % kwargs['verb'], thread)
        models.ThreadLike.vote(thread, request.user, kwargs['verb'])
        return redirect(request.META.get('HTTP_REFERER', reverse_lazy('thread', args=(thread.id, slugify(thread.title)))))


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(models.Post, pk=kwargs['post_id'])
        rules_light.require(request.user, 'askapp.postlike.%s' % kwargs['verb'], post)
        models.PostLike.vote(post, request.user, kwargs['verb'])
        return redirect(request.META.get('HTTP_REFERER', reverse_lazy('thread', args=(post.thread.id, slugify(post.thread.title)))))


class AcceptAnswerView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(models.Post, pk=kwargs['post_id'])
        rules_light.require(request.user, 'askapp.post.accept', post)
        post.accept()
        return redirect(request.META.get('HTTP_REFERER', reverse_lazy('thread', args=(post.thread.id, slugify(post.thread.title)))))


class ThreadFavoriteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        thread = get_object_or_404(models.Thread, pk=kwargs['thread_id'])
        if kwargs['verb'] == 'favorite':
            models.ThreadFavorite.favorite(thread, request.user)
        else:
            models.ThreadFavorite.unfavorite(thread, request.user)
        return redirect(request.META.get('HTTP_REFERER', reverse_lazy('thread', args=(thread.id, slugify(thread.title)))))


class DomainsView(View):
    def domain_stats(self, period, order_by, order_dir):
        params = {'deleted': 0, 'domain__isnull': False}
        dnow = datetime.now()
        if period == 'day':
            params['created__gte'] = dnow - timedelta(days=1)
        elif period == 'week':
            params['created__gte'] = dnow - timedelta(days=7)
        elif period == 'month':
            last_day_previous_month = dnow - timedelta(days=dnow.day)
            params['created__gte'] = (last_day_previous_month.replace(day=dnow.day)
                                     if dnow.day < last_day_previous_month.day
                                     else last_day_previous_month)

        order_fields = ['domain', 'articles', 'avg_points']
        result = models.Thread.objects.filter(**params)\
                            .values('domain')\
                            .annotate(articles=Count('id'))\
                            .annotate(avg_points=Avg('threadlike__points'))\
                            .exclude(domain='')\
                            .values(*order_fields)
        order_by = int(order_by)
        if 0 <= order_by < len(order_fields) and order_fields[order_by]:
            order = order_fields[order_by]
            if order_dir.lower() == 'desc':
                order = '-' + order
            result = result.order_by(order)
        return result[:10]

    def get(self, request, *args, **kwargs):
        context = {
            'period': self.request.GET.get('period', '')
        }
        return render(request, 'domains.html', context)

    def post(self, request, *args, **kwargs):
        period = self.request.POST.get('period', '')
        domains = self.domain_stats(period, self.request.POST.get('order[0][column]', -1),
                                    self.request.POST.get('order[0][dir]', ''))
        data = [[d['domain'], d['articles'], d['avg_points']] for d in domains]
        data = {'draw': self.request.POST.get('draw', 1), 'data': data}
        from django.http import JsonResponse
        return JsonResponse(data)
