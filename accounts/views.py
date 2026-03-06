from django.contrib.auth.hashers import check_password
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AuthToken, User
from .serializers import LoginSerializer, ProfileSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.validated_data['email'])
        except User.DoesNotExist:
            return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active or not check_password(serializer.validated_data['password'], user.password):
            return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_400_BAD_REQUEST)

        token = AuthToken.issue(user)
        return Response({'token': token.key, 'expires_at': token.expires_at})


class LogoutView(APIView):
    def post(self, request):
        token = request.auth
        token.is_revoked = True
        token.save(update_fields=['is_revoked'])
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileView(APIView):
    def get(self, request):
        return Response(ProfileSerializer(request.user).data)

    def patch(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class SoftDeleteView(APIView):
    def post(self, request):
        user = request.user
        user.is_active = False
        user.save(update_fields=['is_active'])
        user.tokens.filter(is_revoked=False).update(is_revoked=True)
        return Response({'detail': 'Аккаунт деактивирован'}, status=status.HTTP_200_OK)
