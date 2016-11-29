from django.db import models
from django.contrib.auth.models import User

from akiba import settings

class Tag(models.Model):
    tag_name = models.CharField(max_length=60, null=False)

class Post(models.Model):

    # codes for types of posts
    QUESTION = "QQ"
    DISCUSSION = "DD"
    LINK = "LL"

    # iterable collection for types of posts
    # must consist of iterables of exactly two items
    TYPES_OF_THREAD = (
        (QUESTION, 'Question'),
        (DISCUSSION, 'Discussion'),
        (LINK, 'Link'),
    )

    # defines the parent post. If the value is null, the post is a thread starter
    parent = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)

    #many to many relationship with tags. When a post is created, it needs to be saved and then tags can be added
    tags = models.ManyToManyField(Tag)

    # these fields are taken into account only if the post is thread starter
    hidden = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    sticky = models.BooleanField(default=False)
    sponsored = models.BooleanField(default=False)

    # reference to the user who created the post
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)


    # atomatically added timestamp field when the record is created
    created = models.DateTimeField(auto_now_add = True)

    # atomatically added timestamp field when the record is modified
    modified = models.DateTimeField(auto_now = True)

    # if the post is the thread starter it must define the thread's type
    thread_type = models.CharField(
        max_length=2,
        choices=TYPES_OF_THREAD,
        default=DISCUSSION,
        null=True
    )

    # post body
    text = models.TextField(null=False)

    # post body with HTML tags
    texthtml = models.TextField(null=True)

    # post title can be null if the post is not a thread starter
    title = models.CharField(max_length=255, null=True)

    image = models.FileField(upload_to='uploads/images/%Y/%m/%d/%H/%M/%S/')




    def __unicode__(self):
        return self.title