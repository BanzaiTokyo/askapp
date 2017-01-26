import datetime
from askapp import models

def calculate_scores():
    """
    calculate and assign scores for threads created within the last 7 days
    Score = (P / T ^G) * 3

    where,
    P = likes minus dislikes
    T = time since submission (in hours), min 1
    G = Gravity, defaults to 1.8
    """

    # get threads that are not older than 7 days
    now = datetime.date.today()
    week_ago = now - datetime.timedelta(weeks=1)

    threads_to_calculate = models.Thread.objects.filter(deleted=False, created__gte=week_ago)

    for current_thread in threads_to_calculate:
        likes = models.ThreadLike.objects.filter(thread=current_thread)

        points = 0
        for like in likes:
            points += like.points

        # calculate the age of the current thread in hours
        age = datetime.datetime.now() - current_thread.created.replace(tzinfo=None)
        age_in_hours = int(age.total_seconds() // 3600)

        if age_in_hours == 0:
            age_in_hours = 1

        score = ((points) / pow(age_in_hours, 1.8)) * 1E+7
        current_thread.score = int(score)

        current_thread.save()
