from datetime import datetime, timedelta
from celery import shared_task
from django.urls import reverse_lazy
from materials.models import Lesson, Subscription
from django.core.mail import send_mail

from users.models import User


@shared_task
def send_email_to_subscribers(lesson_pk, base_url):
    lesson = Lesson.objects.get(pk=lesson_pk)
    emails = [subscription.user.email for subscription in Subscription.objects.filter(course=lesson.course)]
    send_mail(
        "Новый урок!",
        "Ссылка на урок: " + base_url + reverse_lazy("materials:lesson_retrieve", args=[lesson_pk]),
        "from@example.com",
        emails,
        fail_silently=False,
    )


def deactivate_unactive_users():
    users = User.objects.filter(last_login__lt=datetime.now() - timedelta(days=30))
    for user in users:
        user.is_active = False
        user.save()
