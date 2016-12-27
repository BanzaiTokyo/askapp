import rules_light


def can_edit_thread(user, rule, obj):
    return user.is_staff or obj.author == user


def can_reply(user, rule, thread):
    return can_edit_thread(user, rule, thread) and not thread.hidden and not thread.closed

rules_light.registry['akiba.thread.update'] = can_edit_thread
rules_light.registry['akiba.post.create'] = can_reply
