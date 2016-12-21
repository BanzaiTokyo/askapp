from django.conf.urls import include, url
from django.contrib import admin

from akiba import settings
from akiba.views import HomeView, ThreadView, CommentView, AkibaRegistrationView


urlpatterns = [
    url(regex=r'^$',
        view=HomeView.as_view(),
        name="index"),

    url(regex=r'^thread$',
        view=ThreadView.as_view(),
        name="thread"),

    url(regex=r'^comment$',
        view=CommentView.as_view(),
        name="comment"),

    url(r'^accounts/register/$', view=AkibaRegistrationView.as_view()),
    url(r'^accounts/', include('registration.backends.hmac.urls')),

    url(r'^admin/', include(admin.site.urls)),
]

# in debug mode launch debug_toolbar
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
