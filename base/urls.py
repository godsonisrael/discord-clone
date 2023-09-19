from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("register/", views.registerPage, name="register"),
    path("", views.home, name="home"),
    path("room/<str:key>/", views.room, name="room"),
    path("profile/<str:key>/", views.userProfile, name="user-profile"),
    path("create-room/", views.createRoom, name="create-room"),
    path("update-room/<str:key>/", views.updateRoom, name="update-room"),
    path("delete-room/<str:key>/", views.deleteRoom, name="delete-room"),
    path("delete-message/<str:key>/", views.deleteMessage, name="delete-message"),
    path("update-user/", views.updateUser, name="update-user"),
    path("topics/", views.topicsPage, name="topics"),
    path("activity/", views.activityPage, name="activity"),
]
