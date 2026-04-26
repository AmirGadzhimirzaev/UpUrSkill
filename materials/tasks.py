from calendar import month
from datetime import timedelta
from turtledemo.paint import switchupdown

from django.utils import timezone

from celery import shared_task
from django.core.mail import send_mail

from config import settings
from materials.models import Course
from users.models import Subscription, User


@shared_task
def course_update_info_email(pk):
    user_subs = Subscription.objects.filter(sub_course=pk)
    course = Course.objects.get(pk=pk)
    to_email = [email for email in user_subs]

    send_mail(
        f'Обновление курса "{course.name}"',
        f'Здравствуйте, ваш курс "{course.name}" был обновлён!',
        settings.EMAIL_HOST_USER,
        to_email
    )


@shared_task
def check_last_login():
    users_last_login = User.objects.all()
    today = timezone.now()
    for user in users_last_login:
        if user.last_login and user.is_active and today - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()
