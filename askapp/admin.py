from django.contrib import admin
from askapp.models import Profile, Thread, Tag

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'country')


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'num_comments')
    exclude = ('thumbnail', )


class TagAdmin(admin.ModelAdmin):
    exclude = ('slug', )


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Tag, TagAdmin)
