from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db import models
from markdownx.widgets import AdminMarkdownxWidget
from askapp.models import Profile, Thread, Tag, Post

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'id',)



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


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
