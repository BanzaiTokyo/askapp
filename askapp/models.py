import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django_countries.fields import CountryField
from django.core.files.storage import FileSystemStorage
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import ImageFieldFile
from PIL import Image, ImageOps
from mptt.models import MPTTModel, TreeForeignKey
from django.template.defaultfilters import slugify
try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.forms import model_to_dict
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
import rules_light
from markdownx.models import MarkdownxField
from askapp import settings
from siteprefs.models import Preference

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def avatar_name_path(instance, filename):
    extension = filename[filename.rfind('.'):]
    new_path = 'user_profile/%s%s%s' % (instance.user.username, instance.user.pk, extension)
    return new_path


class AskappImageFieldFile(ImageFieldFile):
    @property
    def url(self):
        try:
            result = super(AskappImageFieldFile, self)._get_url()
            if not os.path.isfile(self.path):
                raise ValueError
        except ValueError:
            result = settings.DEFAULT_AVATAR_URL if hasattr(settings, 'DEFAULT_AVATAR_URL') else ''
        return result


class AskappImageField(models.ImageField):
    attr_class = AskappImageFieldFile


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = AskappImageField(storage=OverwriteStorage(), upload_to=avatar_name_path, blank=True)
    country = CountryField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    about = models.TextField(max_length=500, blank=True)

    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)
        self.__original_avatar = self.avatar

    def __unicode__(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email

    def resize_avatar(self):
        # code from with some changes : http://www.yilmazhuseyin.com/blog/dev/create-thumbnails-imagefield-django/
        if not self.avatar:
            return

        try:
            AVATAR_SIZE = settings.AVATAR_SIZE
        except:
            AVATAR_SIZE = (200, 200)

        image = Image.open(BytesIO(self.avatar.read()))
        if self.avatar.name.lower().endswith('png'):
            bg = Image.new("RGB", image.size, (255, 255, 255))
            bg.paste(image, image)
        else:
            bg = image
        min_dimension = min(image.size[0], image.size[1])
        image = ImageOps.fit(bg, (min_dimension, min_dimension))
        image = image.resize(AVATAR_SIZE, Image.ANTIALIAS)

        temp_handle = BytesIO()
        image.save(temp_handle, 'jpeg')
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.avatar.name)[-1], temp_handle.read(), content_type='image/jpeg')
        self.avatar.save('%s.%s' % (os.path.splitext(suf.name)[0], 'jpg'), suf, save=False)

    def save(self, *args, **kwargs):
        if self.avatar != self.__original_avatar:
            self.resize_avatar()
        super(Profile, self).save(*args, **kwargs)

    def get_avatar(self):
        if self.avatar:
            avatar_url = self.avatar.url
        else:
            avatar_url = settings.STATIC_URL + 'images/avatar.png'
        return avatar_url

    @cached_property
    def favorite_threads(self):
        favorites = ThreadLike.objects.filter(user=self.user, points__gt=0).order_by('-created')
        threads = [f.thread for f in favorites]
        return threads


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not instance.is_active:
        if kwargs['update_fields'] and 'is_active' in kwargs['update_fields']:
            # delete user threads and posts
            Post.objects.filter(user_id=instance.id, deleted=False).update(deleted=True)
            Thread.objects.filter(user_id=instance.id, deleted=False).update(deleted=True)
    elif created:
        return Profile.objects.create(user=instance)
    else:
        try:
            profile = instance.profile
        except:
            profile = create_user_profile(None, instance, True)
            instance.profile = profile


class Tag(models.Model):
    name = models.CharField(max_length=60, null=False)
    slug = models.SlugField(max_length=60, null=False)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return "{0}".format(self.name)


class Thread(models.Model):
    # codes for types of posts
    QUESTION = "QQ"
    DISCUSSION = "DD"
    LINK = "LL"

    # iterable collection for types of posts
    # must consist of iterables of exactly two items
    TYPES_OF_THREAD = (
        (QUESTION, _('Question')),
        (DISCUSSION, _('Discussion')),
        (LINK, _('Link')),
    )

    #many to many relationship with tags. When a post is created, it needs to be saved and then tags can be added
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_('tags'))

    # these fields are taken into account only if the post is thread starter
    hidden = models.BooleanField(default=False) # the thread is visible only to the staff and the author
    closed = models.BooleanField(default=False) # noone can post comments / answers in this thread
    sticky = models.DateField(null=True, blank=True) # this thread will be sticky until the given date
    featured = models.BooleanField(default=False) # hopefully one day there will be sponsored threads...
    deleted = models.BooleanField(default=False) # the thread is marked as deleted, usually on user blocking

    # reference to the user who created the post
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

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
    text = MarkdownxField(null=True)

    # link field for the Threads of the type Link
    link = models.URLField(null=True, blank=True)

    # link's domain. Used for /domains page by the task #66
    domain = models.CharField(max_length=255, null=True, blank=True)

    # thread title can be null if the post is not a thread starter
    title = models.CharField(max_length=255, null=True)

    #image that illustrates the thread
    image = models.ImageField(upload_to='uploads/images/%Y/%m/%d', null=True, blank=True)

    #smaller version of the image
    thumbnail = models.ImageField(upload_to='uploads/images/%Y/%m/%d', null=True, blank=True)

    # the current score of the post. It is only calculated for thread posts (no parents)
    # that are not older than one week old
    score = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super(Thread, self).__init__(*args, **kwargs)
        self._old = model_to_dict(self, fields=['id', 'hidden', 'closed', 'sticky', 'sponsored', 'deleted', 'text', 'title'])

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.prepare_images()
        self.update_link()
        super(Thread, self).save()
        AuditThread.audit(self)

    def prepare_images(self):
        if not self.id:
            return
        try:
            this = Thread.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(False)
                this.thumbnail.delete(False)
        except Exception as ex:
            pass

    def update_link(self):
        if self.thread_type != 'LL':
            self.link = None
            self.domain = None
        else:
            hostname = urlparse(self.link)
            self.domain = hostname.netloc

    @property
    def comments(self):
        if self.thread_type == self.QUESTION:
            params = {
                'is_answer': False,
                'deleted': False,
                'parent_id__isnull': True,
            }
            result = self.post_set.filter(**params)
        else:
            result = self.post_set.all()
        return result

    @property
    def answers(self):
        x = self.post_set.filter(is_answer=True, deleted=False)
        return x

    @property
    def num_comments(self):
        return self.post_set.filter(deleted=False).count()

    @property
    def points(self):
        result = self.threadlike_set.all().aggregate(sum=models.Sum('points'))['sum']
        return result or 0

    @property
    def author(self):
        return self.user.username

    @property
    def answered(self):
        return self.answers.filter(accepted__isnull=False).count() > 0


class Post(MPTTModel):
    '''
    Post is a part of the discussion on the levels below Thread
    It can be comments, answers organized in several levels
    '''

    # defines the parent post. If the value is null, the post is a thread starter
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    # the thread that the Post belongs to
    thread = models.ForeignKey(Thread)

    # reference to the user who created the post
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

    # atomatically added timestamp field when the record is created
    created = models.DateTimeField(auto_now_add=True)

    # post body with HTML markup
    text = MarkdownxField(null=True)

    #in question Thread this distinguish answers from comments
    is_answer = models.BooleanField(default=False)

    #the topic starter or the admin selected this post as "the accepted answer"
    accepted = models.DateTimeField(null=True)

    # A post should be marked as deleted instead of physical deletion because it can has live descendant posts
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def points(self):
        result = self.postlike_set.all().aggregate(sum=models.Sum('points'))['sum']
        return result or 0

    @property
    def author(self):
        return self.user.username

    @property
    def comments(self):
        return self.get_children().filter(deleted=False)

    def accept(self):
        self.accepted = datetime.utcnow()
        self.save()


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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)

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
    Users can give up- and down-votes to threads. Upvote = +1, downvote = -1.
    Regular users cannot "like" their own thread.
    Regular users cannot "like" others' threads more than once.
    Threads with positive likes are diplayed in user's "favorites" page.
    '''

    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

    # atomatically added timestamp field when the record is created
    created = models.DateTimeField(auto_now_add=True)

    points = models.IntegerField(default=0)

    @classmethod
    def vote(cls, thread, user, verb):
        points = 1 if verb == 'up' else -1
        kwargs = {'thread': thread, 'user': user}
        try:
            obj = cls.objects.get(**kwargs)
            if not rules_light.registry['askapp.threadlike.%s' % verb](user, None, obj):
                return
        except ObjectDoesNotExist:
            obj = cls(points=0, **kwargs)
        obj.points += points
        obj.save()


class PostLike(models.Model):
    '''

    '''

    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # atomatically added timestamp field when the record is created
    created = models.DateTimeField(auto_now_add=True)

    points = models.IntegerField(default=0)

    @classmethod
    def vote(cls, post, user, verb):
        points = 1 if verb == 'up' else -1
        kwargs = {'post': post, 'user': user}
        try:
            obj = cls.objects.get(**kwargs)
            if not rules_light.registry['askapp.postlike.%s' % verb](user, None, obj):
                return
        except ObjectDoesNotExist:
            obj = cls(points=0, **kwargs)
        obj.points += points
        obj.save()


class AuditThread(models.Model):
    TYPES_OF_ACTION = (
        ("update", 'Update'),
        ("close", 'Close'),
        ("sticky", 'Sticky'),
        ("hide", 'Hide'),
        ("delete", 'Delete'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    thread = models.ForeignKey(Thread)
    action = models.TextField(null=False, choices=TYPES_OF_ACTION, default="update")
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=True)

    @classmethod
    def audit(cls, instance):
        if not instance._old['id'] or not hasattr(instance, 'modified_by'):
            return
        content = None
        if instance._old['deleted'] != instance.deleted:
            action = 'delete'
            content = instance.delete_reason
        elif instance._old['hidden'] != instance.hidden:
            action = 'hide'
        elif instance._old['sticky'] != instance.sticky:
            action = 'sticky'
        elif instance._old['closed'] != instance.closed:
            action = 'close'
        elif instance._old['title'] != instance.title:
            action = 'update'
            content = instance._old['title']
        elif instance._old['text'] != instance.text:
            action = 'update'
            content = instance._old['text']
        else:
            return
        audit = cls(user=instance.modified_by, thread=instance, action=action, content=content)
        audit.save()


@receiver(post_save, sender=Preference)
def clear_language_cache(sender, instance, **kwargs):
    """
    This function clears lru cache of django.utils.translation.trans_real.get_supported_language_variant
    Otherwise this function ignores settings.LANGUAGE_CODE change
    """
    if instance.name == 'language_code':
        from django.utils.translation.trans_real import get_supported_language_variant
        get_supported_language_variant.cache_clear()
