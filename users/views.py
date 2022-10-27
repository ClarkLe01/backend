from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import authentication_classes

from users.models import User, ProfileFeedItem
from users.serializers import UserSerializer, ProfileFeedItemSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import filters
from .permissions import *
from django.contrib import admin
from rest_framework.permissions import IsAuthenticatedOrReadOnly

admin.autodiscover()


class UserViewSetAPI(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [UpdateOwnProfile, ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('email', 'first_name', 'last_name')


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = [TokenAuthentication, ]
    serializer_class = ProfileFeedItemSerializer
    queryset = ProfileFeedItem.objects.all()
    permission_classes = [
        UpdateOwnProfile,
        IsAuthenticatedOrReadOnly,
    ]

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)
