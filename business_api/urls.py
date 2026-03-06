from django.urls import path

from .views import OrdersMockView, ReportsMockView

urlpatterns = [
    path('orders/', OrdersMockView.as_view(), name='orders-mock'),
    path('reports/', ReportsMockView.as_view(), name='reports-mock'),
]
