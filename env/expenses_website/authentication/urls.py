from .views import RegistrationView,UsernameValidationView,EmailValidationView,VerificationView,LoginView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', csrf_exempt(RegistrationView.as_view()), name='register'),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email',csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path('activate/<uidb64>/<token>', csrf_exempt(VerificationView.as_view()), name='activate'),
    path('login', csrf_exempt(RegistrationView.as_view()), name='login'),
]
