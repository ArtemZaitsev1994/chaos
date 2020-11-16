from django.urls import path

from .views import (
    RegistrationAPIView,
    LoginAPIView,
    UserUpdateAPIView
)


app_name = 'authentication-api'
urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration-api'),
    path('login/', LoginAPIView.as_view(), name='login-api'),
    path('user_update/', UserUpdateAPIView.as_view(), name='user-update-api'),

]
