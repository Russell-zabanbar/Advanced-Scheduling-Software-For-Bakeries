from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from accounts.models import CustomUser
from drf_spectacular.utils import extend_schema_field


def clean_phone_number(value):
    if value[:2] != "09":
        raise serializers.ValidationError('شماره تلفن شما باید با 09 شروع شود')
    try:
        int(value)
    except:
        raise serializers.ValidationError('لطفا برای شماره تلفن  فقط از اعداد استفاده کنین')

    return str(value)


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11, min_length=11, validators=[clean_phone_number, ])


class VerificationCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4, min_length=4)

    def validate_code(self, value):
        try:
            int(value)
        except:
            raise serializers.ValidationError('لطفا فقط از اعداد استفاده کنین ')
        return str(value)


class User_Serializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField("get_token")

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'is_baker', 'is_admin', 'token')

    def get_token(self, user) -> dict[str, str]:
        data = dict()
        token_class = RefreshToken

        refresh = token_class.for_user(user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data
