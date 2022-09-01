from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password

User = get_user_model()


class EmailBackend(BaseBackend):
    """Аутентификация по email"""

    def authenticate(self, request, **kwargs):
        email = None
        if 'email' in kwargs:
            email = kwargs['email']

        password = kwargs['password']
        try:
            if email:
                user = User.objects.get(email=email)
            else:
                user = User.objects.get(username=kwargs['username'])
            if check_password(password, user.password) is True:
                return user
        except User.DoesNotExist:
            pass
