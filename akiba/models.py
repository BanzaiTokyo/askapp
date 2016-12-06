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
    parent = models.ForeignKey('self', null=True)

    #many to many relationship with tags. When a post is created, it needs to be saved and then tags can be added
    tags = models.ManyToManyField(Tag)

    # these fields are taken into account only if the post is thread starter
    hidden = models.BooleanField(default=False) # the thread is visible only to the staff and the author
    closed = models.BooleanField(default=False) # noone can post comments / answers in this threa
    sticky = models.DateField(null=True) # this thread will be sticky until the given date
    sponsored = models.BooleanField(default=False) # hopefully one day there will be ponsored threads...

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

    # post body with HTML markup
    texthtml = models.TextField(null=True)

    # post title can be null if the post is not a thread starter
    title = models.CharField(max_length=255, null=True)

    image = models.FileField(upload_to='uploads/images/%Y/%m/%d/%H/%M/%S/')

    # the current score of the post. It is only calculated for thread posts (no parents)
    # that are not older than one week old
    score = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

class Action(models.Model):
    '''
    Actions are taken by users and can describe:
    - update post (saving the old text and title)
    - close post
    - setting post sticky, etc
    '''

    TYPES_OF_ACTION = (
        ("update", 'Update'),
        ("close", 'Close'),
        ("sticky", 'Sticky'),
    )

    takeby_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

    post = models.ForeignKey(Post, null=True)

    # atomatically added timestamp field when the record is created
    taken_on = models.DateTimeField(auto_now_add=True)

    # action
    action_name = models.TextField(null=False, choices=TYPES_OF_ACTION, default="update")

    # old post body with HTML markup
    old_text_html = models.TextField(null=True)

    # old post body
    old_text = models.TextField(null=True)

    # old post title
    old_title = models.TextField(null=True)

