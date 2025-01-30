from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError

from users import constants as cu
from utils import already_use

User = get_user_model()



class BaseAuthSerializer(serializers.Serializer):
    """Базовый сериализатор для регистрации и аутентификации."""

    username = serializers.CharField(max_length=cu.MAX_LENGTH_USERNAME)



class SignUpSerializer(BaseAuthSerializer):
    """Сериализатор для авторизации."""

    telegram_id = serializers.CharField(max_length=30)
    
    def validate(self, attrs):
        return already_use(attrs)

class TokenSerializer(SignUpSerializer):
    """Сериализатор для аутентификации."""

    def validate(self, attrs):
        try:
            User.objects.get(username=attrs['username'])
        except User.DoesNotExist:
            raise NotFound(dict(username='Пользователь не существует'))
        except KeyError as e:
            raise ValidationError(e)
        return attrs


class ImeiSerializer(serializers.Serializer):
    """Сериализатор для обработки и получения информации по IMEI."""
    
    imei = serializers.CharField(min_length=8, max_length=15)
    token = serializers.CharField()
