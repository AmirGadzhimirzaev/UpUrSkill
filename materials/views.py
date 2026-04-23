from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson
from materials.paginations import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer, LessonDetailSerializer, PaymentsSerializer, \
    SubscriptionSerializer
from users.models import Payments, Subscription
from users.permissons import IsModer, IsOwner
from users.services import stripe_product_create, stripe_create_prise, stripe_create_session


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [~IsModer | IsAdminUser | IsAuthenticated, ]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModer | IsAdminUser | IsAuthenticated, ]
    pagination_class = CustomPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsModer | IsOwner | IsAdminUser | IsAuthenticated, ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LessonDetailSerializer
        return LessonSerializer


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModer | IsOwner | IsAdminUser, ]


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [~IsModer | IsOwner | IsAdminUser, ]


class CoursesViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModer | IsAuthenticated,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModer | IsOwner | IsAuthenticated,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner | IsAuthenticated,)
        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'paid_lesson', 'payment_method')
    ordering_fields = ('payment_date',)
    print(queryset[0].course.name)


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        payment.product_id = stripe_product_create(payment.course.name).id
        payment.price_id = stripe_create_prise(payment.product_id, payment.payment_amount).id
        payment.session_id, payment.link, payment.payment_status, payment.currency = stripe_create_session(
            payment.price_id)
        serializer.save()


class PaymentUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


class PaymentDeleteAPIView(generics.DestroyAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, pk=None):
        if pk:
            subs = get_object_or_404(Subscription, pk=pk)
            serializer = SubscriptionSerializer(subs)
            return Response(serializer.data)
        else:
            subscribes = Subscription.objects.all()
            serializer = SubscriptionSerializer(subscribes, many=True)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(sub_user=user, sub_course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'

        else:
            Subscription.objects.create(sub_user=user, sub_course=course_item)
            message = 'подписка добавлена'

        return Response({"message": message})
