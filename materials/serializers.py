from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Lesson, Course
from users.models import Payments


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonDetailSerializer(serializers.ModelSerializer):
    lessons_in_course = SerializerMethodField()

    def get_lessons_in_course(self, lesson):
        return Lesson.objects.filter(course=lesson.course).count()

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'course', 'lessons_in_course')


class CourseSerializer(serializers.ModelSerializer):
    total_lessons_amount = SerializerMethodField()
    lessons_detail = LessonDetailSerializer(source='course', many=True, read_only=True)

    def get_total_lessons_amount(self, course):
        return Lesson.objects.filter(course=course.id).count()

    class Meta:
        model = Course
        fields = ('name', 'total_lessons_amount', 'lessons_detail')


class PaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields = '__all__'