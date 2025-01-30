from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers as sz
from api.utils import get_info

from users.authentication import generate_jwt_token

User = get_user_model()






class SignUpView(APIView):
    """Класс представления для регистрации и получения кода подтверждения."""

    permission_classes = [AllowAny]
    http_method_names = ['post']

    def post(self, request):
        serializer = sz.SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        telegram_id = serializer.validated_data['telegram_id']
        user = User.objects.get_or_create(
            telegram_id=telegram_id,
            username=username)[0]
        user.save()
        return Response(
            dict(telegram_id=user.telegram_id, username=user.username),
            status=status.HTTP_200_OK,
        )


class TokenView(APIView):
    """Класс представления для аутентификации."""

    permission_classes = [AllowAny]
    http_method_names = ['post']

    def post(self, request):
        serializer = sz.TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        user = get_object_or_404(User, username=username)
        user.is_active = True
        user.save()
        token = generate_jwt_token(user)
        return Response({'token': token}, status=status.HTTP_200_OK)


class ImeiView(APIView):
    """Класс представления для получения описания по IMEI."""

    permission_classes = [IsAuthenticated]
    http_method_names = ['post']
    
    def post(self, request):
        serializer = sz.ImeiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        imei = serializer.validated_data['imei']
        token = serializer.validated_data['token']
        data = get_info(imei=imei, token=token)
        return Response(data)