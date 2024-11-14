from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from .models import User
from django.utils import timezone
from djoser.serializers import TokenCreateSerializer as DjoserTokenCreateSerializer
from django.contrib.auth import authenticate


class UserCreateSerializers(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer):
        model = User
        fields = ('id', 'email', 'password')


class ActivationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField(max_length=6)

    def vaidate(self, data):
        try:
            user = User.objects.get(email=data['email'], activation_code=data['activation_code'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or activation code.")

        if user.activation_code_expires < timezone.now():
            raise serializers.ValidationError("Activation code has expired.")

        return data

    def save(self, **kwargs):
        user = User.objects.get(email=self.validated_data['email'])
        user.activation_code = None
        user.activation_code_expires = None
        user.is_active = True
        user.save()
        return user


class CustomTokenCreateSerializer(DjoserTokenCreateSerializer):
    def validate(self, attrs):
        # Аутентифицируем пользователя
        password = attrs.get("password")
        params = {
            'username': attrs.get("username"),
            'email': attrs.get("email"),
        }
        user = authenticate(request=self.context.get('request'), **params, password=password)

        if user and not user.is_active:
            raise serializers.ValidationError("Your account is not activated. Please activate your account.")

        # Продолжаем стандартную проверку Djoser
        return super().validate(attrs)