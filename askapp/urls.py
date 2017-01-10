from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

from askapp import settings
from askapp import views


urlpatterns = [
    # system URLs
    url(r'^admin/', include(admin.site.urls)),

    # static templates
    url(r'^newregister$', views.NewRegisterView.as_view(), name="new_register"),
    url(r'^newlogin$', views.NewLoginView.as_view(), name="new_login"),
    url(r'^thankyou$', views.ThankyouView.as_view(), name="thankyou"),
    url(r'^question$', views.QuestionView.as_view(), name="question"),
    url(r'^comment$', views.CommentView.as_view(), name="comment"),

    # content pages
    url(r'^$', views.HomeView.as_view(), name="index"),
    url(r'^recent$', views.RecentThreadsView.as_view(), name="recent"),
    url(r'^profile/(?P<pk>\d+)$', views.ProfileView.as_view(), name="profile"),
    url(r'^thread/(?P<pk>\d+)$', views.ThreadView.as_view(), name="thread"),
    url(r'^tag/(?P<slug>[-\w]+)$', views.TagView.as_view(), name="tag"),

    url(r'^accounts/register/$', views.AskappRegistrationView.as_view()),
    url(r'^accounts/', include('registration.backends.hmac.urls')),

    # authenticated users
    url(r'^profile/edit$', views.ProfileEditView.as_view(), name="profile_edit"),
    url(r'^profile/(?P<pk>\d+)/edit$', views.AdminProfileEditView.as_view(), name="admin_profile_edit"),
    url(r'^submit$', views.NewThreadView.as_view(), name="new_thread"),
    url(r'^thread/(?P<pk>\d+)/edit$', views.EditThreadView.as_view(), name="edit_thread"),
    url(r'^thread/(?P<pk>\d+)/delete$', views.DeleteThreadView.as_view(), name="delete_thread"),
    url(r'^thread/(?P<thread_id>\d+)/reply$', views.ReplyThreadView.as_view(), name="reply_thread"),
    url(r'^comment/(?P<post_id>\d+)/reply$', views.ReplyCommentView.as_view(), name="reply_comment"),
    url(r'^comment/(?P<post_id>\d+)/delete$', views.DeleteCommentView.as_view(), name="delete_comment"),

    url(r'^thread/(?P<thread_id>\d+)/vote/(?P<verb>up|down)$', views.ThreadLikeView.as_view(), name="thread_like"),
    url(r'^post/(?P<post_id>\d+)/vote/(?P<verb>up|down)$', views.PostLikeView.as_view(), name="post_like"),

]

# in debug mode launch debug_toolbar
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)