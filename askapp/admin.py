from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from askapp.models import Profile, Thread, Tag

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'num_comments')
    exclude = ('thumbnail', )


class TagAdmin(admin.ModelAdmin):
    exclude = ('slug', )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Tag, TagAdmin)
