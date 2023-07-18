from rest_framework.views import APIView
from accounts.serializers import LoginSerializer, VerificationCodeSerializer
from rest_framework.response import Response
from rest_framework import status
import random
from accounts.models import OtpCode
from accounts.models import CustomUser
from django.contrib.auth import login
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.serializers import User_Serializer
from drf_spectacular.utils import extend_schema

class SendOtpCodeApiView(APIView):
    """
    send verification code for user
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        ser_data = LoginSerializer(data=request.data)
        if ser_data.is_valid():
            random_code = random.randint(1000, 9999)
            phone_number = ser_data.data['phone_number']
            print(random_code, phone_number)
            # send_otp_code_sms(...)
            OtpCode.objects.create_otp_code(phone_number=ser_data.data['phone_number'], code=random_code)
            return Response({"message": "send otp code to phone number"}, status.HTTP_200_OK)
        return Response(ser_data.errors, status.HTTP_400_BAD_REQUEST)


class VerificationCodeApiView(APIView):
    """
    verification code and create or login user
    """
    permission_classes = [AllowAny, ]

    @extend_schema(request=VerificationCodeSerializer, responses=User_Serializer)
    def post(self, request):
        permission_classes = [IsAuthenticated, ]

        ser_data = VerificationCodeSerializer(data=request.POST)
        if ser_data.is_valid() and OtpCode.objects.filter(code=ser_data.data['code']).exists():
            otp_object = OtpCode.objects.get(code=ser_data.data['code'])
            if CustomUser.objects.filter(phone_number=otp_object.phone_number).exists():
                user = CustomUser.objects.get(phone_number=otp_object.phone_number)

                user_ser_data = User_Serializer(instance=user)
                login(request, user)
                otp_object.delete()
                return Response({'result': 'your login', 'user_Information': user_ser_data.data}, status.HTTP_200_OK)
            else:
                user = CustomUser.objects.create_user(phone_number=otp_object.phone_number,
                                                      password=None)
                user_ser_data = User_Serializer(instance=user)
                login(request, user)
                otp_object.delete()
                return Response({'result': 'your registered', 'user_information': user_ser_data.data},
                                status.HTTP_200_OK)

        return Response(ser_data.errors, status.HTTP_400_BAD_REQUEST)
