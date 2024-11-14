from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from .models import User


class UserCreateSerializers(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer):
        model = User
        fields = ('id', 'email', 'password')