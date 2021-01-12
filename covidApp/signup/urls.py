from django.urls import path
from signup import views


urlpatterns = [
    path('signUp/', views.SignUpUser.as_view()),
    path('login/', views.LoginUser.as_view())
]