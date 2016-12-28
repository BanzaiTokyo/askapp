import rules_light


def can_edit_thread(user, rule, thread):
    return user.is_staff or thread.user == user


def can_reply(user, rule, thread):
    return can_edit_thread(user, rule, thread) and not thread.hidden and not thread.closed


def can_delete_comment(user, rule, post):
    return user.is_staff or post.user == user


rules_light.registry['akiba.thread.update'] = can_edit_thread
rules_light.registry['akiba.post.create'] = can_reply
rules_light.registry['akiba.post.delete'] = can_delete_comment
