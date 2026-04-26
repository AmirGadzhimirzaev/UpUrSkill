from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Lesson, Course
from materials.validators import validate_accepted_site
from users.models import Payments, Subscription


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_accepted_site], read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonDetailSerializer(serializers.ModelSerializer):
    lessons_in_course = SerializerMethodField()

    def get_lessons_in_course(self, lesson):
        return Lesson.objects.filter(course=lesson.course).count()

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'course', 'lessons_in_course', 'video_url')


class CourseSerializer(serializers.ModelSerializer):
    total_lessons_amount = SerializerMethodField()
    lessons_detail = LessonDetailSerializer(source='course', many=True, read_only=True)

    def get_total_lessons_amount(self, course):
        return Lesson.objects.filter(course=course.id).count()

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'total_lessons_amount', 'lessons_detail')


class CourseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name')


class PaymentsSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(write_only=True)
    amount = serializers.IntegerField(required=True, source='payment_amount')
    course = CourseInfoSerializer(read_only=True)

    class Meta:
        model = Payments
        fields = '__all__'

    def create(self, validated_data):
        course_name = validated_data.pop('course_name')
        course, _ = Course.objects.get_or_create(name=course_name)
        return Payments.objects.create(course=course, **validated_data)


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
