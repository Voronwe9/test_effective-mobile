from rest_framework import authentication, exceptions

from .models import AuthToken


class TokenAuthentication(authentication.BaseAuthentication):
    keyword = 'Token'

    def authenticate_header(self, request):
        return self.keyword

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()
        if not auth:
            return None

        if len(auth) != 2 or auth[0].decode().lower() != self.keyword.lower():
            raise exceptions.AuthenticationFailed('Invalid authorization header')

        token_key = auth[1].decode()
        try:
            token = AuthToken.objects.select_related('user').get(key=token_key)
        except AuthToken.DoesNotExist as exc:
            raise exceptions.AuthenticationFailed('Invalid token') from exc

        if not token.is_valid:
            raise exceptions.AuthenticationFailed('Token expired or revoked')

        return token.user, token
