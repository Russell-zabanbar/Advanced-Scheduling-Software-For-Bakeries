from django.test import TestCase, Client
from accounts.serializers import LoginSerializer, VerificationCodeSerializer
from django.urls import reverse
from accounts.models import OtpCode

class TestOtpCode(TestCase):
    def setUp(self):
        self.client = Client()

    def test_serializer_login(self):
        ser_date = LoginSerializer(data={'phone_number': '09012844143'})
        self.assertTrue(ser_date.is_valid())
        ser_date = LoginSerializer(data={'phone_number': '90128441433'})
        self.assertFalse(ser_date.is_valid())
        ser_date = LoginSerializer(data={'phone_number': '0901s84414d'})
        self.assertFalse(ser_date.is_valid())

    def test_verification_serializer(self):
        ser_data = VerificationCodeSerializer(data={'code': '1234'})
        self.assertTrue(ser_data.is_valid())
        ser_data = VerificationCodeSerializer(data={'code': '1d3g'})
        self.assertFalse(ser_data.is_valid())

    def test_SendOtpCodeApiView(self):
        response = self.client.post(reverse('jwt:send_otp_code'), data={'phone_number': '09012844143'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('jwt:send_otp_code'), data={'phone_number': '0901s84d143'})
        self.assertEqual(response.status_code, 400)

    def test_model_str(self):
        otp_code = OtpCode.objects.create_otp_code(phone_number='09012844143', code=1234)
        self.assertEqual(str(otp_code), '09012844143')



