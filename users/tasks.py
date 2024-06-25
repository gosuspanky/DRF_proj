from datetime import datetime, timedelta

from users.models import User
from celery import shared_task


@shared_task
def check_activity():
    users_list = User.objects.all()

    for user in users_list:
        last_login_date = user.last_login
        date_now = datetime.now()
        time_difference = last_login_date - date_now
        if time_difference > timedelta(days=30):
            user.is_active = False
            user.save()
