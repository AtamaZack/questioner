from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.Login.as_view(), name='login'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path("profile/", views.profile.as_view(), name="profile"),
    path('users/', views.Users.as_view(), name='users'),
    path("session/signup/", views.SignUp.as_view(), name="signup2"),
    path("session/profile/", views.profile.as_view(), name="profile"),

]
