from django.conf import settings
from django.conf.urls.static import static
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import include, path
from member import views

app_name = 'member'

# apiview 방식

urlpatterns = [
    # auth
    path('login/token/', views.TokenLoginView.as_view()),
    path('logout/', views.UserLogoutView.as_view()),

    # user
    path('create/', views.UserCreateView.as_view()),
    path('detail/<int:pk>/', views.UserRetrieveUpdateDestroyView.as_view()),
    path('detail/<int:pk>/update/', views.UserRetrieveUpdateDestroyView.as_view()),
    path('detail/<int:pk>/delete/', views.UserRetrieveUpdateDestroyView.as_view()),
]