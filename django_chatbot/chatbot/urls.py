from django.urls import path
from .import views

urlpatterns=[
    path('', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('chatbot/',views.chatbot,name='chatbot'),
    path('logout/', views.logout, name='logout'),
    path('user_dash/', views.user_dash, name='dashboard'),
    path('profile/', views.profile, name='profile'), 
    # path('home/', views.home, name='home'),
    # path('user_dash/', views.user_dash, name='dashboard'),
]