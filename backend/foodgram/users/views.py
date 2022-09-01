from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import SubscribersByCurrentUser
from .permissions import SubscribeToYourself
from .serializers import (ChangePasswordSerializer,
                          MyTokenObtainPairSerializer, RegisterUserSerializer,
                          UserSerializer, UserSerializerSubscribers)
from food.filters import RecipeFilter
from food.views import CustomPageNumberPagination

User = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):
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

        user = User.objects.get(username=request.user)
        serializer = UserSerializer(user, data=request.data, context={
                                    'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """Регистрация пользователя"""

        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        if serializer.is_valid():
            user.set_password(serializer.data.get("new_password"))
            print(serializer.data.get("new_password"))
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddSubscribe(APIView):
    """Подписка на автора"""

    permission_classes = [SubscribeToYourself]

    def post(self, request, pk, format=None):
        user = get_object_or_404(
            User, pk=pk)

        # For has_object_permission on create
        # https://www.django-rest-framework.org/api-guide/generic-views/#get_objectself
        self.check_object_permissions(self.request, user)

        add_subscribe, created = (
            SubscribersByCurrentUser.objects.get_or_create(
                current_user=self.request.user, subscription=user))
        if created is False:
            raise ValidationError(
                {'detail': 'Пользователь уже находится в списке подписок'})

        recipe_serializer = UserSerializerSubscribers(
            user, context={'request': request})
        return Response(recipe_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        user = get_object_or_404(
            User, pk=pk)

        add_to_subscribe = SubscribersByCurrentUser.objects.filter(
            current_user=self.request.user, subscription=user)
        if add_to_subscribe:
            add_to_subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"errors": "Подписка отсутсвует"},
                        status=status.HTTP_400_BAD_REQUEST)
