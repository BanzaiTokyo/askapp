from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models
from markdownx.widgets import AdminMarkdownxWidget
from askapp.models import Profile, UserLevel, Thread, Tag, Post, ThreadLike, Token
from django.db.models import Value, CharField
from django.shortcuts import render
from django.urls import path
from django.utils.safestring import mark_safe
from django.apps.registry import apps
from askapp import settings


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

    def has_add_permission(self, request, obj=None):
        return False


class TokenInline(admin.StackedInline):
    model = Token

    class Media:
        js = ('js/admin.js', )


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, TokenInline)
    ordering = ('-date_joined',)
    list_display = ('username', 'first_name', 'last_name', 'email', 'id','date_joined')


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('created', 'author', 'title', 'score', 'points', 'num_comments')
    list_display_links = ('title',)
    ordering = ('-created',)
    exclude = ('thumbnail', )
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }


class PostAdmin(admin.ModelAdmin):
    list_display = ('created', 'text', 'author')
    list_display_links = ('text',)
    ordering = ('-created',)
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }


class TagAdmin(admin.ModelAdmin):
    exclude = ('slug', )


def combined_recent(limit, **kwargs):
    datetime_field = kwargs.pop('datetime_field', 'created')
    querysets = []
    for key, queryset in kwargs.items():
        querysets.append(
            queryset.annotate(
                recent_changes_type=Value(
                    key, output_field=CharField()
                )
            ).values('pk', 'recent_changes_type', datetime_field)
        )
    union_qs = querysets[0].union(*querysets[1:])
    records = []
    for row in union_qs.order_by('-{}'.format(datetime_field))[:limit]:
        records.append({
            'type': row['recent_changes_type'],
            'when': row[datetime_field],
            'pk': row['pk']
        })
    # Now we bulk-load each object type in turn
    to_load = {}
    for record in records:
        to_load.setdefault(record['type'], []).append(record['pk'])
    fetched = {}
    for key, pks in to_load.items():
        for item in kwargs[key].filter(pk__in=pks):
            fetched[(key, item.pk)] = item
    # Annotate 'records' with loaded objects
    for record in records:
        record['object'] = fetched[(record['type'], record['pk'])]
    return records


def audit_view(request, model_admin):
    show_tech = request.GET.get('show_tech') == 'true'
    if show_tech:
        log = combined_recent(
            limit=settings.AUDIT_LOG_SIZE,
            threadlike=ThreadLike.objects.all(),
            thread=Thread.objects.all(),
            comment=Post.objects.all(),
        )
    else:
        log = combined_recent(
            limit=settings.AUDIT_LOG_SIZE,
            threadlike=ThreadLike.objects.exclude(user_id=settings.TECH_USER),
            thread=Thread.objects.exclude(user_id=settings.TECH_USER),
            comment=Post.objects.exclude(user_id=settings.TECH_USER),
        )
    opts = model_admin.model._meta
    app_config = apps.get_app_config(opts.app_label)
    context = {
        **model_admin.admin_site.each_context(request),
        "opts": opts,
        "app_config": app_config,
        "results": log,
        "show_tech": show_tech
    }
    template_name = "admin/askapp/audit.html"
    return render(request, template_name, context)


class AuditModel(models.Model):
    class Meta:
        verbose_name_plural = 'Activity log'
        app_label = 'askapp'


class AuditModelAdmin(admin.ModelAdmin):
    model = AuditModel

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('activity_log', audit_view, name=view_name, kwargs={"model_admin": self}),
        ]

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True


class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'upvotes', 'downvotes', 'upvote_same', 'downvote_same')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(AuditModel, AuditModelAdmin)
admin.site.register(UserLevel, LevelAdmin)
