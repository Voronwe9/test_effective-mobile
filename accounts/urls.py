from django.urls import path

from .views import LoginView, LogoutView, ProfileView, RegisterView, SoftDeleteView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('delete/', SoftDeleteView.as_view(), name='delete'),
]
