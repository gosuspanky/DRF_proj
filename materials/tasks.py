from config import settings
from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_info_about_update(email):
    subject = "Обновление курса"
    message = f"Пользователь {email} обновил свой курс"
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        settings.RECIPIENT_LIST,
        fail_silently=False,
    )
