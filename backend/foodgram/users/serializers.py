from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ValidationError

from .models import FavoritedRecipesByUser, SubscribersByCurrentUser
from food.serializers import AddedFavoriteSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор вывода данных пользователя"""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name',
            'last_name', 'is_subscribed',
        ]

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        if SubscribersByCurrentUser.objects.filter(
                current_user=user, subscription=obj).exists():
            return True
        return False


class RegisterUserSerializer(serializers.ModelSerializer):
    """Сериализатор регистрация пользователя"""

    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(
        label=("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'password'
        ]

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password'))
        return super(RegisterUserSerializer, self).create(validated_data)

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return email


class UserSerializerSubscribers(serializers.ModelSerializer):
    """Сериализатор моих подписок"""

    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    recipes = AddedFavoriteSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'recipes',

        ]


class MyTokenObtainPairSerializer(serializers.Serializer):
    """Выдача токена авторизации"""

    email = serializers.CharField(
        label=("email"),
        write_only=True
    )
    password = serializers.CharField(
        label=("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                raise ValidationError({'detail': 'Пользователь не найден'})

            # Структра отправки для токена
            data = {}
            token, created = Token.objects.get_or_create(user=user)
            data['auth_token'] = str(token.key)
            return data
        raise ValidationError({'detail': 'email и password обязательные поля'})


class FavoritedRecipesByUserSerializer(serializers.ModelSerializer):
    """Избранные рецепты"""
    class Meta:
        fields = ('author', 'recipe')
        model = FavoritedRecipesByUser


class ChangePasswordSerializer(serializers.Serializer):
    """Изменение пароля"""

    new_password = serializers.CharField()
    current_password = serializers.CharField()

    def validate(self, attrs):
        current_password = attrs.get('current_password')
        new_password = attrs.get('new_password')

        user = self.context['request'].user
        if not check_password(current_password, user.password):
            raise ValidationError({'detail': 'Текущий пароль не верен'})
        validate_password(new_password)
        return attrs
