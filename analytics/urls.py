from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('coach/', views.ai_coach, name='ai_coach'),
]
