from django.urls import path, include
from accounts.views import SendOtpCodeApiView, VerificationCodeApiView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('send_code/', SendOtpCodeApiView.as_view(), name='send_otp_code'),
    path('check_code/', VerificationCodeApiView.as_view(), name='verification_code'),
    path('refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),


]

