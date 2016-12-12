from django.db import models
from django.contrib.auth.models import User

from akiba import settings

class Tag(models.Model):
    tag_name = models.CharField(max_length=60, null=False)

class Thread(models.Model):

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

    # Thread must have one of the types defined in TYPES_OF_THREAD
    thread_type = models.CharField(
        max_length=2,
        choices=TYPES_OF_THREAD,
        default=DISCUSSION,
        null=True
    )

    # thread body with HTML markup
    text = models.TextField(null=True)

    # link field for the Threads of the type Link
    link = models.TextField(null=True)

    # thread title can be null if the post is not a thread starter
    title = models.CharField(max_length=255, null=True)

    #image that illustrates the thread
    image = models.FileField(upload_to='uploads/images/%Y/%m/%d/%H/%M/%S/')

    #smaller version of the image
    thumbnail = models.FileField(upload_to='uploads/images/%Y/%m/%d/%H/%M/%S/', null=True)

    # the current score of the post. It is only calculated for thread posts (no parents)
    # that are not older than one week old
    score = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

class Post(models.Model):
    '''
    Post is a part of the discussion on the levels below Thread
    It can be comments, answers organized in several levels
    '''

    # defines the parent post. If the value is null, the post is a thread starter
    parent = models.ForeignKey('self', null=True)

    # the thread that the Post belongs to
    thread_id = models.ForeignKey(Thread, null=True)

    # atomatically added timestamp field when the record is created
    created = models.DateTimeField(auto_now_add = True)

    # post body with HTML markup
    text = models.TextField(null=True)

    #in question Thread, the topic starter or the admin can select one of the answers as "the answer"
    the_answer = models.BooleanField(default=False)

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

    taken_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

    post = models.ForeignKey(Post, null=True)

    # atomatically added timestamp field when the record is created
    taken_on = models.DateTimeField(auto_now_add=True)

    # action
    action_name = models.TextField(null=False, choices=TYPES_OF_ACTION, default="update")

    # old post body
    old_text = models.TextField(null=True)

    # old post title
    old_title = models.TextField(null=True)

class ThreadLike(models.Model):
    '''

    '''

    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

    # atomatically added timestamp field when the record is created
    created = models.DateTimeField(auto_now_add=True)

    points = models.IntegerField()


class PostLike(models.Model):
    '''

    '''

    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

    # atomatically added timestamp field when the record is created
    created = models.DateTimeField(auto_now_add=True)

    points = models.IntegerField()