from django.urls import path
from .views import UserCreateAPIView, UserLoginAPIView, UserStatusCreateAPIView


urlpatterns = [
    path(
        'register/',
        UserCreateAPIView.as_view(),
        name='register'
    ),

    path(
        'login/',
        UserLoginAPIView.as_view(),
        name='login'
    ),

    path(
        'status/',
        UserStatusCreateAPIView.as_view(),
        name='post_status'
    ),
]
