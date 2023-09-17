from django.urls import path
from .views import *
urlpatterns = [
    path("login/",LoginView.as_view(), name="login"),
    path("forgot-password/",ForgotPasswordView.as_view(), name="forgot_password"),
    path("reset-password/<token>/",ResetPasswordView.as_view(), name="reset_password"),
    path("change-password/",ChangePasswordView.as_view(), name="change_password"),
    path("profile/",ProfileView.as_view(),name="profile"),
    path('check-token/', CheckTokenValidityView.as_view(), name='check-token'),
    path("send-otp/", SendOTPView.as_view(), name="send_otp"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify_otp"),
    path("login/google/", GoogleLogin.as_view(), name="google_login")
]