"""
View for user API
"""
from django.contrib.auth import get_user_model
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics, authentication, permissions
from users.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.ListCreateAPIView):
    """View to create a user"""
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class AllUsersView(generics.RetrieveAPIView):
    """APIView to retrieve all users"""
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

class CreateTokenView(ObtainAuthToken):
    """APIView to create a token for a user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageAuthUserView(generics.RetrieveUpdateAPIView):
    """APIView to manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """"""
        return self.request.user
