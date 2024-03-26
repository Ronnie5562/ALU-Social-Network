"""
URL mapping for user API.
"""
from django.urls import path
from users import views

app_name = 'user'

urlpatterns = [
    path('', views.CreateUserView.as_view(), name='list-create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('<int:pk>/', views.AllUsersView.as_view(), name='user'),
    path('me/', views.ManageAuthUserView.as_view(), name='me'),
]
