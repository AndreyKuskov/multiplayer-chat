from django.urls import path
from django.conf import settings
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
	path('', views.HomeView.as_view(), name="chat"),
 	path('register/', views.RegisterView.as_view(), name='register'),
	path('logout/', views.Logout.as_view(), name='logout'),
	path('<str:room_name>/', views.RoomView.as_view(), name='room'),
]
