from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from materials.views import PaymentCreateAPIView, PaymentListAPIView, PaymentUpdateAPIView, PaymentDeleteAPIView
from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserListAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('list/', UserListAPIView.as_view(), name='user-list'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('payment/', PaymentCreateAPIView.as_view(), name='payment'),
    path('payment/list/', PaymentListAPIView.as_view(), name='payment-list'),
    path('payment/update/<int:pk>', PaymentUpdateAPIView.as_view(), name='payment-update'),
    path('payment/delete/<int:pk>', PaymentDeleteAPIView.as_view(), name='payment-delete'),
]