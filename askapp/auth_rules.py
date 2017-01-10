import rules_light
from askapp.models import ThreadLike, PostLike

def can_edit_thread(user, rule, thread):
    return user.is_staff or thread.user == user


def can_reply(user, rule, thread):
    return can_edit_thread(user, rule, thread) and not thread.hidden and not thread.closed


def can_delete_comment(user, rule, post):
    return user.is_staff or post.user == user


def can_vote_thread(user, rule, thread):
    return user.is_active and thread.user != user and ThreadLike.objects.filter(thread=thread, user=user).count() == 0


def can_vote_post(user, rule, post):
    return user.is_active and post.user != user and PostLike.objects.filter(post=post, user=user).count() == 0

def can_edit_profile(user, rule, user_object):
    return user.is_staff


rules_light.registry['askapp.thread.update'] = can_edit_thread
rules_light.registry['askapp.post.create'] = can_reply
rules_light.registry['askapp.post.delete'] = can_delete_comment
rules_light.registry['askapp.threadlike.create'] = can_vote_thread
rules_light.registry['askapp.postlike.create'] = can_vote_post
rules_light.registry['askapp.profile.update'] = can_edit_profile
