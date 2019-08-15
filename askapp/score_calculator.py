from django.db import connection
from askapp import models

GRAVITY = 1.8
MAGNIFIER = 1E+7


def calculate_scores(weeks=100):
    """
    calculate and assign scores for threads created within the last 7 days
    Score = (P / T^G) * M

    where,
    P = likes minus dislikes
    T = time since submission (in hours), min 1
    G = Gravity
    M = Magnifier, a multiplying coefficient
    """

    sql = f"""
        UPDATE {models.Thread._meta.db_table} t 
        LEFT JOIN (SELECT thread_id, SUM(points) as points 
              FROM {models.ThreadLike._meta.db_table} l 
              GROUP BY thread_id) l
        ON t.id = l.thread_id
        SET score = IFNULL(l.points, 0) / POW(GREATEST(TIMESTAMPDIFF(HOUR, t.created, now()), 1), {GRAVITY}) * {MAGNIFIER}
        WHERE t.deleted = 0
    """
    if weeks:
        # get threads that are not older than X weeks
        sql += f" AND t.created >= DATE_SUB(now(), INTERVAL {int(weeks)} WEEK)"

    with connection.cursor() as cursor:
        result = cursor.execute(sql)
        print(f"{result} threads updated")
