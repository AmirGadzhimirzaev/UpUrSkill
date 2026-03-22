from datetime import datetime

from django.core.management import BaseCommand
from django.utils import timezone

from materials.models import Course, Lesson
from users.models import Payments, User


class Command(BaseCommand):
    help = 'Add test payment in DB'

    def handle(self, *args, **kwargs):

        user = User.objects.get(id=1)
        paid_course = Course.objects.get(id=2)
        paid_lesson = Lesson.objects.get(id=2)
        paid_lesson_1 = Lesson.objects.get(id=3)
        paid_lesson_2 = Lesson.objects.get(id=4)

        payments = [
            {
                'user': user, 'payment_date': timezone.make_aware(datetime(2025, 3, 15, 9, 0)),
                'paid_course': paid_course,
                'paid_lesson': paid_lesson,
                'payment_amount': 10000,
                'payment_method': 'наличные'
            },
            {
                'user': user, 'payment_date': timezone.make_aware(datetime(2024, 2, 15, 9, 0)),
                'paid_course': paid_course,
                'paid_lesson': paid_lesson_1,
                'payment_amount': 12000,
                'payment_method': 'перевод на карту'
            },
            {
                'user': user,
                'payment_date': timezone.make_aware(datetime(2023, 1, 15, 9, 0)),
                'paid_course': paid_course,
                'paid_lesson': paid_lesson_2,
                'payment_amount': 14000, 'payment_method': 'наличные'
            },
        ]

        for payment in payments:
            payment, created = Payments.objects.get_or_create(**payment)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added payment: {payment.user}'))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Payment already exists: {payment.user} - {payment.paid_lesson} - {payment.payment_amount}'))
