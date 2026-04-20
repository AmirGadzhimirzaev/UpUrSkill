from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import CoursesViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonDestroyAPIView, LessonUpdateAPIView, PaymentListAPIView, SubscriptionAPIView

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register(r'course', CoursesViewSet, basename='course')

urlpatterns = [
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-retrieve'),
    path('lesson/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
    path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('subscription/', SubscriptionAPIView.as_view(), name='subscription-list'),
    path('subscription/<int:pk>/', SubscriptionAPIView.as_view(), name='subscription-delete'),
]

urlpatterns += router.urls