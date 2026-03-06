from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from access_control.services import user_has_access


class OrdersMockView(APIView):
    def get(self, request):
        if not user_has_access(request.user, 'orders', 'read'):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return Response([
            {'id': 1, 'name': 'Order #1'},
            {'id': 2, 'name': 'Order #2'},
        ])


class ReportsMockView(APIView):
    def get(self, request):
        if not user_has_access(request.user, 'reports', 'read'):
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return Response([
            {'id': 1, 'title': 'Sales Report'},
        ])
