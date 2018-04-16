from django.contrib.auth import authenticate
from django.utils import timezone

from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer, UserProfileSerializer
from django.contrib.auth.models import User
from .models import UserProfile, UserToken, AppToken
from .app_token_auth import AppTokenAuthentication

import binascii
import os


class UserTokenView(APIView):
    authentication_classes = (AppTokenAuthentication, )

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if (username is None or password is None):
            return Response({'error': 'Need username and password data'}, status=400)
        user = authenticate(username=username, password=password)
        if user is None:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            new_token = binascii.hexlify(os.urandom(15)).decode('ascii')
            tok, created = UserToken.objects.update_or_create(
                user=user,
                defaults={
                    'user': user,
                    'token': new_token,
                    'expires': timezone.now() + timezone.timedelta(minutes=5)},
            )
            return Response({'token': new_token})


class UserTokenCheckView(APIView):
    authentication_classes = (AppTokenAuthentication, )

    def post(self, request):
        username = request.data['username']
        token = request.data['token']
        try:
            tok = UserToken.objects.get(token=token, user__username=username)
        except UserToken.DoesNotExist:
            return Response(status=401)
        if tok.expires < timezone.now():
            return Response(status=401)
        else:
            tok.expires = timezone.now() + timezone.timedelta(minutes=5)
            tok.save()
            return Response(status=200)


class AppTokenView(APIView):
    def get(self, request):
        clientId = request.query_params.get('clientId')
        clientSecret = request.query_params.get('clientSecret')
        try:
            tok = AppToken.objects.get(client_id=clientId, client_secret=clientSecret)
        except AppToken.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)
        new_token = binascii.hexlify(os.urandom(15)).decode('ascii')
        tok.token = new_token
        tok.expires = timezone.now() + timezone.timedelta(minutes=5)
        tok.save()
        return Response({'token': new_token})


class UserViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    authentication_classes = (AppTokenAuthentication, )


class ProfileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = (AppTokenAuthentication, )