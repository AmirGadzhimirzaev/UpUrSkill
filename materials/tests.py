from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User, Subscription


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="test@test.ru", password='1234')
        self.course = Course.objects.create(name='Java', description='Popular programing language')
        self.lesson = Lesson.objects.create(name='Numbers', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), self.course.name
        )

    def test_course_create(self):
        url = reverse("materials:course-list")
        data = {
            "name": "Форест"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            Course.objects.all().count(), 2
        )

    def test_course_update(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {
            "name": "JS"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "JS"
        )

    def test_course_delete(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Course.objects.all().count(), 0
        )

    def test_course_list(self):
        url = reverse("materials:course-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.course.pk,
                    'name': self.course.name,
                    'total_lessons_amount': 1,
                    'lessons_detail': [
                        {
                            'id': self.lesson.pk,
                            'name': self.lesson.name,
                            'course': self.course.pk,
                            'lessons_in_course': 1,
                            'video_url': None
                        }
                    ]
                }
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )


class LessonsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="test@test.ru", password='1234')
        self.course = Course.objects.create(name='Go', description='Popular programing language')
        self.lesson = Lesson.objects.create(name='Arrays', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), self.lesson.name
        )

    def test_lesson_create(self):
        url = reverse("materials:lesson-create")
        data = {
            "name": "Build-ins"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {
            "name": "Lists"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "Lists"
        )

    def test_lesson_delete(self):
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse("materials:lesson-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.lesson.pk,
                    'video_url': None,
                    'name': self.lesson.name,
                    'description': None,
                    'preview': None,
                    'course': 9,
                    'owner': self.user.id,
                }
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='subs_testuser@test.ru', password='1234')
        self.anonymous_user = None

        self.course = Course.objects.create(name='PHP', description='old but strong language')
        self.subs = Subscription.objects.create(sub_user=self.user, sub_course=self.course)
        self.subs_anonym = Subscription.objects.create(sub_user=self.anonymous_user, sub_course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_subs_list(self):
        url = reverse("materials:subscription-list")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

    def test_subs_create(self):
        url = reverse("materials:subscription-list")
        data = {
            "course_id": self.course.pk
        }
        response = self.client.post(url, data)
        data = {
            "message": "подписка удалена"
        }
        result = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )

    def test_subs_delete(self):
        url_create = reverse("materials:subscription-list")
        url_delete = reverse("materials:subscription-delete", args=[self.subs.pk])

        data = {
            "course_id": self.course.pk
        }
        response = self.client.post(url_create, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.client.post(url_delete)
        data = {
            "message": "подписка удалена"
        }
        result = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )

    def test_anonymous_cannot_list(self):
        self.client.force_authenticate(user=self.anonymous_user)
        url = reverse("materials:subscription-list")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )
