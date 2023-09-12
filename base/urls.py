from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('', views.home, name="home"),
    path('room/<str:key>/', views.room, name='room'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:key>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:key>/', views.deleteRoom, name='delete-room'),
]
