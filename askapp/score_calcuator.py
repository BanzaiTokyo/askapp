import datetime
from askapp import models

def get_age_in_hours(thread):
    age = datetime.datetime.now() - thread.created.replace(tzinfo=None)
    age_hours = int(age.total_seconds() // 3600)
    return age_hours

def calculate_scores():
    """
    calculate and assign scores for threads created within the last 7 days
    Score = (P / T ^G) * 3

    where,
    P = likes minus dislikes
    T = time since submission (in hours), min 1
    G = Gravity, defaults to 1.8
    """
    now = datetime.date.today()
    week_ago = now - datetime.timedelta(weeks=1)

    # get threads created in the last 7 days
    threads_to_calculate = models.Thread.objects.filter(deleted=False, created__gte=week_ago)

    for current_thread in threads_to_calculate:
        likes = models.ThreadLike.objects.filter(thread=current_thread)
        points = len(likes)
        age_in_hours = get_age_in_hours(current_thread)
        if age_in_hours == 0:
            age_in_hours = 1

        score = ((points) / pow(age_in_hours, 1.8)) * 3
        current_thread.score = score + 1
        current_thread.save()
        print("points", current_thread.score, "age: ", age_in_hours)
