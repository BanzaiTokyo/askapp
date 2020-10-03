import os
import logging

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
import re
import requests

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
    """
    When saving an image, this storage class deletes existing file, thus implementing the overwriting feature
    """
    def get_available_name(self, name, *args, **kwargs):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def avatar_name_path(instance, filename):
    """
    convert arbitrary file name to the string consisting of username and user ID
    """
    extension = filename[filename.rfind('.'):]
    new_path = 'user_profile/%s%s%s' % (instance.user.username, instance.user.pk, extension)
    return new_path


def favorite_threads(user):
    """
    get list of the threads that user has "upvoted"
    """
    favorites = ThreadLike.objects.filter(user=user, points__gt=0).order_by('-created')
    threads = [f.thread for f in favorites]
    return threads


class AskappImageFieldFile(ImageFieldFile):
    """
    Return default avatar if there is no image
    """
    @property
    def url(self):
        try:
            result = super(AskappImageFieldFile, self).url
            if not os.path.isfile(self.path):
                raise ValueError
        except ValueError:
            result = settings.DEFAULT_AVATAR_URL if hasattr(settings, 'DEFAULT_AVATAR_URL') else ''
        return result


class AskappImageField(models.ImageField):
    attr_class = AskappImageFieldFile


class UserLevel(models.Model):
    """
    User "level" object. Shows how many articles a user with this level can upvote/downvote
    """

    name = models.CharField(blank=False, max_length=100)  # level name
    upvotes = models.IntegerField(default=3, verbose_name='Upvotes per day')  # how many articles a user can upvote per day
    downvotes = models.IntegerField(default=0)
    upvote_same = models.IntegerField(default=1, verbose_name='Upvotes of the same article')  # can user upvote the same article multiple times?
    downvote_same = models.IntegerField(default=1, verbose_name='Downvote same article')

    def __str__(self):
        return str(self.name)


class Profile(models.Model):
    """
    Additional user properties. Attached to the Django user object by 1-to-1 relation
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 1-to-1 relation to the builtin Django User object
    avatar = AskappImageField(storage=OverwriteStorage(), upload_to=avatar_name_path, blank=True)
    country = CountryField(blank=True)  # country of residence. 3rd party component, saved as ISO code, displayed as full name. Input control is a dropdown list, supporting localisation
    city = models.CharField(max_length=50, blank=True)  # city of residence
    about = models.TextField(max_length=500, blank=True)  # "about me", biography text field
    level = models.ForeignKey(UserLevel, on_delete=models.DO_NOTHING, null=True, default=1)  #  user level, kinda "permissions" in the system

    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)
        # __original_avatar is used to detect avatar change, to run avatar resize procedure only when needed
        self.__original_avatar = self.avatar

    def __unicode__(self):
        return self.user.username

    @cached_property
    def email(self):
        """
        a helper that allows get email even from the Profile object
        """
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

    @cached_property
    def favorite_threads(self):
        return favorite_threads(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    if hasattr(instance, 'profile') and instance.profile:
        instance.profile.save()
    elif not created:
        create_user_profile(sender, instance, created=True, **kwargs)


@receiver(post_save, sender=User)
def delete_user_content(sender, instance, created, **kwargs):
    """
     Signal handler running after Django.user object is saved.
     For disabled user it marks as "deleted" all user's threads and posts
    """
    if not instance.is_active:
        if kwargs['update_fields'] and 'is_active' in kwargs['update_fields']:
            # Perform posts/threads deletion only when is_active field was explicitly mentioned for update
            # delete user threads and posts
            Post.objects.filter(user_id=instance.id, deleted=False).update(deleted=True)
            Thread.objects.filter(user_id=instance.id, deleted=False).update(deleted=True)


class Tag(models.Model):
    """
    Thread tags
    """
    name = models.CharField(max_length=60, null=False)  # full tag name
    slug = models.SlugField(max_length=60, null=False)  # slugified tag name to use in URLs

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return "{0}".format(self.name)


class Thread(models.Model):
    """
    Thread is the main content object of the application
    """
    # codes for types of posts
    QUESTION = "QQ"
    DISCUSSION = "DD"
    LINK = "LL"
    YOUTUBE = "YT"
    DUPLICATE = "DU"
    VIDEOSTREAM = "VS"

    # iterable collection for types of posts
    # must consist of iterables of exactly two items
    TYPES_OF_THREAD = (
        #(QUESTION, _('Question')),
        (DISCUSSION, _('Discussion')),
        (LINK, _('Link')),
        (YOUTUBE, _('Youtube video')),
        (DUPLICATE, _('Duplicate thread')),
        (VIDEOSTREAM, _('Video stream')),
    )
    TYPES_WITH_LINK = [LINK, YOUTUBE, DUPLICATE, VIDEOSTREAM]

    #many to many relationship with tags. When a post is created, it needs to be saved and then tags can be added
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_('tags'))

    # these fields are taken into account only if the post is thread starter
    hidden = models.BooleanField(default=False)  # the thread is visible only to the staff and the author
    closed = models.BooleanField(default=False)  # no one can post comments / answers in this thread
    sticky = models.DateField(null=True, blank=True)  # this thread will be sticky until the given date
    featured = models.BooleanField(default=False)  # hopefully one day there will be sponsored threads...
    deleted = models.BooleanField(default=False)  # the thread is marked as deleted, usually on user blocking

    # reference to the user who created the post
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, default=1)

    # atomatically added timestamp field when the record is created
    created = models.DateTimeField(auto_now_add=True)

    # atomatically added timestamp field when the record is modified
    modified = models.DateTimeField(auto_now=True)

    # Thread must have one of the types defined in TYPES_OF_THREAD
    thread_type = models.CharField(
        max_length=2,
        choices=TYPES_OF_THREAD,
        default=LINK,
        null=True
    )

    # thread body with HTML markup
    text = MarkdownxField(null=True)

    # link field for the Threads of the type Link
    link = models.URLField(null=True, blank=True, unique=True)

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

    # when thread type is "duplicate" this is a link to the original, "main" thread
    original = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL)

    def __init__(self, *args, **kwargs):
        super(Thread, self).__init__(*args, **kwargs)
        self._old = model_to_dict(self, fields=['id', 'hidden', 'closed', 'sticky', 'sponsored', 'deleted', 'text', 'title'])

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.prepare_images()
        self.update_link()
        super(Thread, self).save()
        AuditThread.audit(self)  # log all changes applied to the thread

    def _delete_old_image(self):
        try:
            this = Thread.objects.get(id=self.id)
            if this.image != self.image:
                # delete old image explicitly, as new image will have different name
                this.image.delete(False)
                this.thumbnail.delete(False)
        except Exception as ex:
            pass

    @cached_property
    def youtube_id(self):
        # url = url.split(/(vi\/|v%3D|v=|\/v\/|youtu\.be\/|\/embed\/)/);
        # return undefined !== url[2]?url[2].split(/[^0-9a-z_\-]/i)[0]:url[0];
        r = r"(vi\/|v%3D|v=|\/v\/|youtu\.be\/|\/embed\/)"
        video_id = re.split(r, self.link)
        if len(video_id) == 3:
            video_id = re.split(r"[^0-9a-z_\-](?i)", video_id[2])
        else:
            return None
        return video_id[0] if video_id else None

    def parse_youtube_url(self):
        id = self.youtube_id
        item = {}
        if id and settings.GOOGLE_API_KEY:
            snippet = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={id}&key={settings.GOOGLE_API_KEY}')
            snippet = snippet.json()
            if snippet.get('items'):
                item = snippet['items'][0]['snippet']
                item['image'] = item['thumbnails']['default']['url']
        if not item and id:  # failed to get video info from googleapis, trying 3rd party service
            snippet = requests.get(f'https://noembed.com/embed?url=https://www.youtube.com/watch?v={id}')
            snippet = snippet.json()
            if snippet.get('title'):
                item = snippet
                item['image'] = item['thumbnail_url']
                item['description'] = ''
        result = {'id': id} if id else None
        if item:
            result.update(**{k: item[k] for k in ['title', 'description', 'image']})
        return result

    def _load_youtube_thumbnail(self):
        yt_info = self.parse_youtube_url()
        if yt_info:
            filename = os.path.basename(yt_info['image'])
            ext = filename.split('.', 1)[-1]
            filename = '%s.%s' % (yt_info['id'], ext)
            response = requests.get(yt_info['image'])
            self.image = SimpleUploadedFile(filename, response.content, response.headers['content-type'])

    def prepare_images(self):
        if self.thread_type == self.YOUTUBE and not self.image:
            self._load_youtube_thumbnail()
        if not self.id:
            return
        self._delete_old_image()

    def update_link(self):
        """
        extract domain name for threads of type "link"
        """
        if self.thread_type not in self.TYPES_WITH_LINK:
            self.link = None
        if self.thread_type not in [self.LINK, self.DUPLICATE]:
            self.domain = None
        else:
            hostname = urlparse(self.link)
            self.domain = hostname.netloc

    @cached_property
    def comments(self):
        if self.thread_type == self.QUESTION:  # filter out comments marked as answers, they'll come in another property
            params = {
                'is_answer': False,
                'deleted': False,
                'parent_id__isnull': True,
            }
            result = self.post_set.filter(**params)
        else:
            result = self.post_set.all()
        return result

    @cached_property
    def answers(self):
        x = self.post_set.filter(is_answer=True, deleted=False)
        return x

    @cached_property
    def num_comments(self):
        return self.post_set.filter(deleted=False).count()

    @cached_property
    def points(self):
        result = self.threadlike_set.all().aggregate(sum=models.Sum('points'))['sum']
        return result or 0

    @cached_property
    def author(self):
        return self.user.username

    @cached_property
    def answered(self):
        """
        check whether the thread of type "question" has an answer, to prevent marking another comment as the answer
        """
        return self.answers.filter(accepted__isnull=False).count() > 0

    @cached_property
    def duplicates(self):
        if self.original:
            q = models.Q(original__in=[self.original.id, self.id]) | models.Q(id=self.original.id)
            q = q & ~models.Q(id=self.id)
        else:
            q = models.Q(original=self.id)
        return Thread.objects.filter(q, deleted=False)


class Post(MPTTModel):
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    """
    Post is a part of the discussion on the levels below Thread
    It can be comments, answers organized in several levels
    """

    # defines the parent post. If the value is null, the post is a thread starter
    parent = TreeForeignKey('self', models.CASCADE, null=True, blank=True, related_name='children', db_index=True)

    # the thread that the Post belongs to
    thread = models.ForeignKey(Thread, models.CASCADE)

    # reference to the user who created the post
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, default=1)

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

    @cached_property
    def points(self):
        result = self.postlike_set.all().aggregate(sum=models.Sum('points'))['sum']
        return result or 0

    @cached_property
    def author(self):
        return self.user.username

    @cached_property
    def comments(self):
        return self.get_children().filter(deleted=False)

    def accept(self):
        """
        accept this comment as the answer for the thread type "question"
        """
        self.accepted = datetime.utcnow()
        self.save()


class ThreadLike(models.Model):
    """
    Users can give up- and down-votes to threads. Upvote = +1, downvote = -1.
    Regular users cannot "like" their own thread.
    Regular users cannot "like" others' threads more than once.
    Threads with positive likes are diplayed in user's "favorites" page.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, default=1)
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
        except ObjectDoesNotExist:
            obj = cls(points=0, **kwargs)
        if (not rules_light.registry['askapp.threadlike.%s' % verb](user, None, thread)
            or not rules_light.registry['askapp.user.%svote_threads' % verb](user, None)
        ):
            return obj
        obj.points += points
        obj.created = datetime.utcnow()
        obj.save()
        return obj


class PostLike(models.Model):
    """
    Users can give up- and down-votes to comments. Upvote = +1, downvote = -1.
    Regular users cannot "like" their own comments.
    Regular users cannot "like" others' comments more than once.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, default=1)
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
            if not rules_light.registry['askapp.postlike.%s' % verb](user, None, post):
                return obj
        except ObjectDoesNotExist:
            obj = cls(points=0, **kwargs)
        obj.points += points
        return obj


class AuditThread(models.Model):
    """
    Audit user actions
    Actions are taken by users and can describe:
    - update post (saving the old text and title)
    - close post
    - setting post sticky, etc
    """

    TYPES_OF_ACTION = (
        ("update", 'Update'),
        ("close", 'Close'),
        ("sticky", 'Sticky'),
        ("hide", 'Hide'),
        ("delete", 'Delete'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, default=1)
    thread = models.ForeignKey(Thread, models.CASCADE)
    action = models.TextField(null=False, choices=TYPES_OF_ACTION, default="update")
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=True)  # old title or text of the edited post

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
    Otherwise Django ignores settings.LANGUAGE_CODE change
    """
    if instance.name == 'language_code':
        from django.utils.translation.trans_real import get_supported_language_variant
        get_supported_language_variant.cache_clear()
