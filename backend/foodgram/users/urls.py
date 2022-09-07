from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AddSubscribe, ChangePassword, Login, Logout, SubscriptionViewSet,
    UserViewSet
)

app_name = 'users'

router = DefaultRouter()
router.register('users/subscriptions', SubscriptionViewSet,
                basename='subscriptions')
router.register('users', UserViewSet, basename='users')


auth_endpoints = [
    path(
        'token/login/',
        Login.as_view(),
        name='login'
    ),
    path(
        'token/logout/',
        Logout.as_view(),
        name='logout'
    ),

]
urlpatterns = [
    path('users/<int:pk>/subscribe/', AddSubscribe.as_view()),
    path('auth/', include(auth_endpoints)),
    path('users/set_password/', ChangePassword.as_view(), name='set_password'),
    path('', include(router.urls)),

]
