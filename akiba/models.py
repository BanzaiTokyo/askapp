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
import urlparse
from django.core.exceptions import ObjectDoesNotExist

from akiba import settings


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def avatar_name_path(instance, filename):
    extension = filename[filename.rfind('.'):]
    new_path = 'user_profile/%s%s%s' % (instance.user.username, instance.user.pk, extension)
    return new_path


class AkibaImageFieldFile(ImageFieldFile):
    @property
    def url(self):
        try:
            result = super(AkibaImageFieldFile, self)._get_url()
        except ValueError:
            result = settings.STATIC_URL + 'images/avatar.png'
        return result


class AkibaImageField(models.ImageField):
    attr_class = AkibaImageFieldFile


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = AkibaImageField(storage=OverwriteStorage(), upload_to=avatar_name_path, blank=True)
    country = CountryField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    about = models.TextField(max_length=500, blank=True)

    def __unicode__(self):
        return self.user.username

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
        self.resize_avatar()
        super(Profile, self).save()

    def get_avatar(self):
        if self.avatar:
            avatar_url = self.avatar.url
        else:
            avatar_url = settings.STATIC_URL + 'images/avatar.png'
        return avatar_url


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.is_active:
        return Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        profile = instance.profile
    except:
        if instance.is_active:
            profile = create_user_profile(None, instance, True)
            instance.profile = profile
    else:
        profile.save()


class Tag(models.Model):
    name = models.CharField(max_length=60, null=False)
    slug = models.SlugField(max_length=60, null=False)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)


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
    text = models.TextField(null=True)

    # link field for the Threads of the type Link
    link = models.URLField(null=True, blank=True)

    # thread title can be null if the post is not a thread starter
    title = models.CharField(max_length=255, null=True)

    #image that illustrates the thread
    image = models.ImageField(upload_to='uploads/images/%Y/%m/%d', null=True, blank=True)

    #smaller version of the image
    thumbnail = models.ImageField(upload_to='uploads/images/%Y/%m/%d', null=True, blank=True)

    # the current score of the post. It is only calculated for thread posts (no parents)
    # that are not older than one week old
    score = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.prepare_images()
        super(Thread, self).save()

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

    @property
    def comments(self):
        return self.post_set.all()

    @property
    def num_comments(self):
        return Post.objects.filter(thread=self, deleted=False).count()

    @property
    def domain(self):
        if not hasattr(self, '_domain'):
            self._domain = None
            if self.link:
                hostname = urlparse.urlparse(self.link)
                self._domain = hostname.netloc
        return self._domain

    @property
    def points(self):
        result = self.threadlike_set.all().aggregate(models.Sum('points'))
        return result.values()[0] or 0


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
    text = models.TextField(null=True)

    #in question Thread, the topic starter or the admin can select one of the answers as "the answer"
    the_answer = models.BooleanField(default=False)

    # A post should be marked as deleted instead of physical deletion because it can has live descendant posts
    deleted = models.BooleanField(default=False)

    @property
    def points(self):
        result = self.postlike_set.all().aggregate(models.Sum('points'))
        return result.values()[0] or 0


@receiver(pre_delete, sender=Post)
def _post_delete(sender, instance, **kwargs):
    if not instance.deleted:
        instance.thread.num_comments -= 1
        instance.thread.save()


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
        except ObjectDoesNotExist:
            obj = cls(points=points, **kwargs)
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
        except ObjectDoesNotExist:
            obj = cls(points=points, **kwargs)
            obj.save()
