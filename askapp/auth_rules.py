import rules_light
from askapp.models import ThreadLike, PostLike
from datetime import datetime, timedelta
from .settings import UPVOTES_PER_DAY

def can_edit_thread(user, rule, thread):
    return user.is_staff or thread.user == user


def can_delete_thread(user, rule, thread):
    return user.is_staff


def can_reply_thread(user, rule, thread):
    return user.is_active and not thread.hidden and not thread.closed and not thread.deleted


def can_reply_post(user, rule, post):
    return can_reply_thread(user, rule, post.thread) and (post.thread.thread_type != post.thread.QUESTION or
                                                          post.get_level() == 0)


def can_delete_comment(user, rule, post):
    return user.is_staff or post.user == user


def can_delete_comment_tree(user, rule, post):
    return user.is_staff


def can_upvote_threads(user, rule):
    return ThreadLike.objects.filter(user=user, created__gte=datetime.utcnow()-timedelta(days=1)).count() < int(str(UPVOTES_PER_DAY))\
        or user.is_staff


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


def can_accept_answer(user, rule, post):
    return can_reply_thread(user, rule, post.thread) and (user.is_staff or post.thread.user == user) \
            and not post.thread.answered and post.get_level() == 0


def can_edit_profile(user, rule, user_object):
    return user.is_staff


rules_light.registry['askapp.thread.update'] = can_edit_thread
rules_light.registry['askapp.thread.delete'] = can_delete_thread
rules_light.registry['askapp.post.create'] = can_reply_thread
rules_light.registry['askapp.post.reply'] = can_reply_post
rules_light.registry['askapp.post.accept'] = can_accept_answer
rules_light.registry['askapp.post.delete'] = can_delete_comment
rules_light.registry['askapp.post.delete_all'] = can_delete_comment_tree
rules_light.registry['askapp.user.upvote_threads'] = can_upvote_threads
rules_light.registry['askapp.threadlike.up'] = can_like_thread
rules_light.registry['askapp.threadlike.down'] = can_dislike_thread
rules_light.registry['askapp.postlike.up'] = can_like_post
rules_light.registry['askapp.postlike.down'] = can_dislike_post
rules_light.registry['askapp.profile.update'] = can_edit_profile
