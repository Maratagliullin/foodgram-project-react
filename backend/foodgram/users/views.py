from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import SubscribersByCurrentUser
from .serializers import (
    ChangePasswordSerializer, DeleteSubscribeUser, MyTokenObtainPairSerializer,
    RegisterUserSerializer, SubscribeUser, UserSerializer,
    UserSerializerSubscribers
)
from foods.filters import RecipeFilter
from foods.views import CustomPageNumberPagination

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Операции связананные с Users"""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPagination

    def get_permissions(self):
        """Раздаем права на просмотр пользователей
        и регисирацию пользователей"""

        if self.action in ('create', 'list'):
            self.permission_classes = [AllowAny, ]
        return super(self.__class__, self).get_permissions()

    def get_queryset(self):
        return User.objects.all()

    @action(
        detail=False, methods=['GET'], url_path='me',
        permission_classes=[IsAuthenticated]
    )
    def me_user(self, request, pk=None):
        """Обработка узла users/me"""

        serializer = UserSerializer(request.user, data=request.data, context={
                                    'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Регистрация пользователя"""

        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscriptionViewSet(viewsets.ModelViewSet):
    """Мои подписки"""

    serializer_class = UserSerializerSubscribers
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        current_user = self.request.user
        subscribers = current_user.subscribers.values_list('subscription')
        return User.objects.filter(
            id__in=subscribers)

    def get_serializer_context(self):
        return {'request': self.request}


class Login(TokenObtainPairView):
    """Обработка выдачи токенов."""

    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer


class Logout(APIView):
    """Выход пользоватля из системы."""

    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePassword(APIView):
    """Изменение пароля."""

    def post(self, request):
        user = self.request.user
        serializer = ChangePasswordSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.data.get('new_password'))
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddSubscribe(APIView):
    """Подписка на автора"""

    def post(self, request, pk, format=None):
        user = get_object_or_404(
            User, pk=pk)

        serializer = SubscribeUser(
            data={}, context={'request': request, 'user': user})
        serializer.is_valid(raise_exception=True)

        add_subscribe = (
            SubscribersByCurrentUser(
                current_user=self.request.user, subscription=user))
        add_subscribe.save()

        recipe_serializer = UserSerializerSubscribers(
            user, context={'request': request})
        return Response(recipe_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        user = get_object_or_404(
            User, pk=pk)

        serializer = DeleteSubscribeUser(
            data={}, context={'request': request, 'user': user})
        serializer.is_valid(raise_exception=True)

        add_to_subscribe = SubscribersByCurrentUser.objects.filter(
            current_user=self.request.user, subscription=user)
        add_to_subscribe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
