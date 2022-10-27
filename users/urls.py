from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'users'

router = DefaultRouter(app_name)
router.register('users', UserViewSetAPI)
router.register('feed', UserProfileFeedViewSet)
urlpatterns = [
    path('', include(router.urls), name='users'),
    path('login/', UserLoginApiView.as_view(), name='login'),
]
