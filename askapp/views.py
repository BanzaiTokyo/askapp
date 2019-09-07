from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from registration.backends.default.views import RegistrationView
from django.conf import settings
from askapp import forms, models
from askapp.settings import BLACKLISTED_DOMAINS, REGISTRATION_OPEN, SITE_NAME
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.db.models import ObjectDoesNotExist
from django.http import Http404, HttpResponseBadRequest
from django.template.defaultfilters import slugify
from django.urls import resolve
from django.db.models import Q, Count, Avg
from memoize import memoize
from django.http import JsonResponse

from datetime import datetime, timedelta
from collections import namedtuple

import rules_light
import askapp.auth_rules
import logging


class LoginRequiredMixin(object):
    """
    A common ancestor for the class-based views that require authentication
    """
    def dispatch(self, request, *args, **kwargs):
        """
        it's a standard Django method that is called before HTTP methods
        """
        if request.user.is_authenticated and request.user.is_active:
            return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


class HomeView(View):
    """
    Home page handler. Additionally, this is the base class to display a page that "should look like the home page"
    """
    def get_threads(self):
        """
        Returns the list of threads to display on the page. This function is overwritten in descendant classes
        """
        # pick up non-sticky or old sticky threads
        result = models.Thread.objects.filter( Q(sticky__isnull=True) | Q(sticky__lt=datetime.now()), deleted=False).order_by('-score')
        return result[:10]

    def get_sticky(self):
        """
        Returns the list of sticky threads
        """
        return models.Thread.objects.filter(deleted=False, sticky__isnull=False, sticky__gte=datetime.now())

    def get(self, request, *args, **kwargs):
        context = {
            'home_page': resolve(request.path_info).url_name == 'index'
        }
        context.update({
            'threads': self.get_threads(),
            'sticky': self.get_sticky() if context['home_page'] or self.request.GET.get('page', '1') == '1' else [],
            'tags': models.Tag.objects.all(),
            'users': models.User.objects.filter(is_active=True).order_by('-date_joined')[:5],
        })
        return render(request, 'index.html', context)


class RecentThreadsView(HomeView):
    """
    /recent page handler
    """
    def get_threads(self):
        # exclude sticky threads from the first page (they are displayed in a separate list)
        if self.request.GET.get('page', '1') == '1':
            return models.Thread.objects.filter( Q(sticky__isnull=True) | Q(sticky__lt=datetime.now()), deleted=False).order_by('-created')
        else:
            return models.Thread.objects.filter(deleted=False).order_by('-created')


class FavoriteThreadsView(View):
    """
    /favorites page handler
    """
    def get(self, request, *args, **kwargs):
        context = {
            'home_page': False,
            'threads': self.request.user.profile.favorite_threads if hasattr(self.request.user, 'profile') else [],
        }
        return render(request, 'favorites.html', context)


class ProfileView(DetailView):
    model = models.User
    template_name = 'profile.html'

    def get_context_object_name(self, obj):
        """
        Return the context variable name that will be used to contain the data that this view is manipulating.
        Named it "object" to align with other templates
        """
        return 'object'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['threads'] = models.Thread.objects.filter(user=self.object, deleted=False).order_by('-created')
        context['per_page'] = settings.PAGINATION_THREADS_PER_PROFILE
        context['admin_view'] = self.request.user.is_staff
        try:
            context['favorites'] = self.object.profile.favorite_threads if self.request.user.is_authenticated else None
        except models.Profile.DoesNotExist:
            context['favorites'] = None
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    /profile/edit page handler
    """
    form_class = forms.ProfileForm
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('profile_edit')

    def get_object(self, queryset=None):
        try:
            profile = self.request.user.profile
        except:  # this is just for an improbable case when the user object has no corresponding profile object
            return models.Profile.objects.model(user=self.request.user)
        return profile


@rules_light.class_decorator('askapp.profile.update')
class AdminProfileEditView(LoginRequiredMixin, UpdateView):
    """
    /profile/:id/edit handler - edit arbitrary profile by admins
    """
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
            # update everything, except is_active to prevent deleting user's threads/posts on this step
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
    """
    Displays single thread view of all three types: Question, Link, Discussion
    In case of "question" type of thread thread_question.html is used
    """
    model = models.Thread

    def get_template_names(self):
        return 'thread_question.html' if self.object.thread_type == self.object.QUESTION else 'thread.html'


class AskappRegistrationView(RegistrationView):
    """
    /account/register page handler
    """
    form_class = forms.RecaptchaRegistrationForm
    template_name = 'registration_form.html'

    def registration_allowed(self):
        """
        This method returns proper settings.REGISTRATION_OPEN value when used with django-siteprefs
        """
        return REGISTRATION_OPEN.get_value() if isinstance(REGISTRATION_OPEN, object) else REGISTRATION_OPEN

    @staticmethod
    def is_email_blacklisted(email):
        return any([email.lower().endswith('@'+d) for d in BLACKLISTED_DOMAINS])

    def get_email_context(self, activation_key):
        """
        populate template variables for the activation email
        """
        result = super(AskappRegistrationView, self).get_email_context(activation_key)
        d = {'domain': self.request.get_host(), 'name': SITE_NAME}
        result['site'] = namedtuple("Site", d.keys())(*d.values())
        return result

    def send_activation_email(self, user):
        if self.is_email_blacklisted(user.email):
            logging.debug('blacklisted email %s', user.email)
        else:
            super(AskappRegistrationView, self).send_activation_email(user)


class ThreadMixin(object):
    """
    Common methods for create/edit threads
    """
    form_class = forms.ThreadForm
    template_name = 'thread_edit.html'
    def get_form_kwargs(self):
        kwargs = super(ThreadMixin, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('thread', args=(self.object.id, slugify(self.object.title)))


class NewThreadView(LoginRequiredMixin, ThreadMixin, CreateView):
    """
    /submit page handler
    """
    pass


@rules_light.class_decorator('askapp.thread.update')
class EditThreadView(LoginRequiredMixin, ThreadMixin, UpdateView):
    """
    /thread/:id/:slug/edit page handler
    """
    model = models.Thread

    def get_context_data(self, **kwargs):
        context = super(EditThreadView, self).get_context_data(**kwargs)
        context['admin_view'] = self.request.user.is_staff
        return context


@rules_light.class_decorator('askapp.thread.delete')
class DeleteThreadView(LoginRequiredMixin, UpdateView):
    """
    /thread/:id/:slug/delete page handler
    """
    success_url = reverse_lazy('index')
    model = models.Thread
    fields = ['deleted']
    template_name = 'thread_delete.html'

    def form_valid(self, form):
        """
        This function is used to avoid placing <input type="hidden" name="deleted"/> to the page. Instead, it explicitly
        sets the value of "deleted" attribute
        """
        instance = form.save(commit=False)
        instance.deleted = True
        instance.delete_reason = self.request.POST.get('reason', '')
        return super(DeleteThreadView, self).form_valid(form)


class LockThreadView(LoginRequiredMixin, View):
    """
    /thread/:id/:slug/lock|unlock handler. Todo: refactor thread locking to AJAX?
    """
    def get(self, request, *args, **kwargs):
        thread = get_object_or_404(models.Thread, pk=kwargs['thread_id'])
        rules_light.require(request.user, 'askapp.thread.update', thread)  # check user credentials to update the thread
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
    Inline comment handler, /thread/:id/:slug/reply
    """
    template_name = 'index.html'

    def form_invalid(self, form):
        # fail silently, redirect back to the thread view
        return redirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        # redirect to the thread view in case this URL is opened directly. Do not display empty home page
        return redirect(self.get_success_url())


class ReplyCommentView(ReplyMixin):
    """
    Standalone comment handler, /comment/:id
    """
    template_name = 'comment.html'

    def get_form(self, form_class=None):
        post_id = self.kwargs.get('post_id')
        self.post_object = get_object_or_404(models.Post, pk=post_id)
        self.kwargs['thread_id'] = self.post_object.thread.id  # for get_success_url()
        return super(ReplyCommentView, self).get_form(form_class)

    def get_context_data(self, **kwargs):
        context = super(ReplyCommentView, self).get_context_data(**kwargs)
        context['object'] = self.post_object
        return context

    def form_valid(self, form):
        form.instance.parent = self.post_object
        return super(ReplyCommentView, self).form_valid(form)


class DeleteCommentView(LoginRequiredMixin, View):
    """
    Actually this is not a view, but just a request handler for /comment/:id/delete
    """
    def get(self, request, *args, **kwargs):
        # no need to display the post deletion confirmation, so use GET method instead of POST
        post = get_object_or_404(models.Post, pk=kwargs['post_id'])
        rules_light.require(request.user, 'askapp.post.delete', post)
        post.deleted = True
        post.save()
        return redirect(reverse_lazy('thread', args=(post.thread.id, slugify(post.thread.title))))


class DeleteCommentTreeView(LoginRequiredMixin, View):
    """
    /comment/:id/delete_all handler
    """
    def get(self, request, *args, **kwargs):
        rules_light.require(request.user, 'askapp.post.delete_all', None)
        post = get_object_or_404(models.Post, pk=kwargs['post_id'])
        post.get_descendants(include_self=True).update(deleted=1)
        return redirect(reverse_lazy('thread', args=(post.thread.id, slugify(post.thread.title))))


class TagView(HomeView):
    """
    Display threads by tag, /tag/:slug handler
    """
    def get_threads(self):
        try:
            tag = models.Tag.objects.get(slug=self.kwargs['slug'])
        except ObjectDoesNotExist:
            return []
        return tag.thread_set.order_by('-created')


class ThreadLikeView(LoginRequiredMixin, View):
    """
    /thread/:id/:slug/vote/up|down handler. Todo: refactor for AJAX?
    """
    def get(self, request, *args, **kwargs):
        thread = get_object_or_404(models.Thread, pk=kwargs['thread_id'])
        rules_light.require(request.user, 'askapp.threadlike.%s' % kwargs['verb'], thread)
        tl = models.ThreadLike.vote(thread, request.user, kwargs['verb'])
        if 'application/json' in request.META.get('CONTENT_TYPE', '').lower():
            return JsonResponse({'points': tl.points})
        else:
            return redirect(request.META.get('HTTP_REFERER',
                                             reverse_lazy('thread', args=(thread.id, slugify(thread.title)))))


class PostLikeView(LoginRequiredMixin, View):
    """
    /post/:id/:slug/vote/up|down handler. Todo: refactor for AJAX?
    """
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(models.Post, pk=kwargs['post_id'])
        rules_light.require(request.user, 'askapp.postlike.%s' % kwargs['verb'], post)
        pl = models.PostLike.vote(post, request.user, kwargs['verb'])
        if 'application/json' in request.META.get('CONTENT_TYPE', '').lower():
            return JsonResponse({'points': pl.points})
        else:
            return redirect(request.META.get('HTTP_REFERER',
                                             reverse_lazy('thread', args=(post.thread.id, slugify(post.thread.title)))))


class AcceptAnswerView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(models.Post, pk=kwargs['post_id'])
        rules_light.require(request.user, 'askapp.post.accept', post)
        post.accept()
        return redirect(request.META.get('HTTP_REFERER', reverse_lazy('thread', args=(post.thread.id, slugify(post.thread.title)))))


class DomainsView(View):
    """
    /domains page handler, displays number of articles and average "like" points for domain names extracted from
    threads of type "link"
    """
    # cache the results for 1 day. Caching decorator considers the method parameters, so different caches for each
    # period and ordering column will be created
    @memoize(timeout=86400)
    def domain_stats(self, period, order_by, order_dir):
        params = {'deleted': 0, 'domain__isnull': False}
        dnow = datetime.utcnow()
        if period == 'day':
            params['created__gte'] = dnow - timedelta(days=1)
        elif period == 'week':
            params['created__gte'] = dnow - timedelta(days=7)
        elif period == 'month':
            # gets the day one month ago (taking into account edge cases)
            last_day_previous_month = dnow - timedelta(days=dnow.day)
            params['created__gte'] = (last_day_previous_month.replace(day=dnow.day)
                                     if dnow.day < last_day_previous_month.day
                                     else last_day_previous_month)

        display_fields = ['domain', 'articles', 'avg_points']
        result = models.Thread.objects.filter(**params)\
                            .values('domain')\
                            .annotate(articles=Count('id'))\
                            .annotate(avg_points=Avg('threadlike__points'))\
                            .exclude(domain='')\
                            .values(*display_fields)
        order_by = int(order_by)
        if 0 <= order_by < len(display_fields) and display_fields[order_by]:
            order = display_fields[order_by]
            if order_dir.lower() == 'desc':
                order = '-' + order
            result = result.order_by(order)
        if hasattr(settings, 'NUM_DOMAIN_STATS'):
            #int(str()) converts the setting from django-siteprefs object back to its original type
            result = result[:int(str(settings.NUM_DOMAIN_STATS) or 10)]
        return result

    def get(self, request, *args, **kwargs):
        context = {
            'period': self.request.GET.get('period', '')
        }
        return render(request, 'domains.html', context)

    def post(self, request, *args, **kwargs):
        """
        server part of the Datatables component
        """
        period = self.request.POST.get('period', '')
        domains = self.domain_stats(period, self.request.POST.get('order[0][column]', -1),
                                    self.request.POST.get('order[0][dir]', ''))
        data = [[d['domain'], d['articles'], d['avg_points']] for d in domains]
        data = {'draw': self.request.POST.get('draw', 1), 'data': data}
        return JsonResponse(data)


class DomainThreadsView(HomeView):
    """
    /domains/:domain handler, displays list of threads for a domain
    """
    def get_threads(self):
        domain = self.kwargs.get('domain')
        if not domain:
            return redirect(reverse_lazy('domains'))
        return models.Thread.objects.filter(domain=domain)

    def get_sticky(self):
        return None


class YoutubeInfo(View):
    def get(self, request, *args, **kwargs):
        yt_url = request.GET.get('q', '')
        data = models.Thread(link=yt_url).parse_youtube_url()
        if data:
            return JsonResponse(data)
        return HttpResponseBadRequest('This URL does not seem a valid YouTube link')
