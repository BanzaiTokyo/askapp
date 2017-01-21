import rules_light
from askapp.models import ThreadLike, PostLike

def can_edit_thread(user, rule, thread):
    return user.is_staff or thread.user == user


def can_delete_thread(user, rule, thread):
    return user.is_staff


def can_reply(user, rule, thread):
    return not thread.hidden and not thread.closed and not thread.deleted


def can_delete_comment(user, rule, post):
    return user.is_staff or post.user == user


def can_like_thread(user, rule, thread):
    return user.is_active and thread.user != user and ThreadLike.objects.filter(thread=thread, user=user).count() == 0 \
            or user.is_staff


def can_dislike_thread(user, rule, thread):
    return user.is_staff


def can_like_post(user, rule, post):
    return user.is_active and post.user != user and PostLike.objects.filter(post=post, user=user).count() == 0 \
            or user.is_staff

def can_dislike_post(user, rule, post):
    return user.is_staff


def can_edit_profile(user, rule, user_object):
    return user.is_staff


rules_light.registry['askapp.thread.update'] = can_edit_thread
rules_light.registry['askapp.thread.delete'] = can_delete_thread
rules_light.registry['askapp.post.create'] = can_reply
rules_light.registry['askapp.post.delete'] = can_delete_comment
rules_light.registry['askapp.threadlike.up'] = can_like_thread
rules_light.registry['askapp.threadlike.down'] = can_dislike_thread
rules_light.registry['askapp.postlike.up'] = can_like_post
rules_light.registry['askapp.postlike.down'] = can_dislike_post
rules_light.registry['askapp.profile.update'] = can_edit_profile
