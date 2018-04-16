from django.utils import timezone
from rest_framework import authentication, exceptions
from .models import AppToken

class AppTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = str(request.META.get('HTTP_AUTHORIZATION')).split()[-1]
        if token == 'None':
            raise exceptions.AuthenticationFailed('No app token')
        try:
            tok = AppToken.objects.get(token=token)
        except AppToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('No app with such token')

        if tok.expires < timezone.now():
            raise exceptions.AuthenticationFailed('App token expired')
        return (None, None)

    def authenticate_header(self, request):
        return 'AppTokenAuthentication'