from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from askapp.models import Profile, Thread, Tag, Post

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('created', 'author', 'title', 'score', 'num_points', 'num_comments')
    list_display_links = ('title',)
    ordering = ('-created',)
    exclude = ('thumbnail', )

class PostAdmin(admin.ModelAdmin):
    list_display = ('created', 'text', 'author')
    list_display_links = ('text',)
    ordering = ('-created',)

class TagAdmin(admin.ModelAdmin):
    exclude = ('slug', )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
