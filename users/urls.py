from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="User_Register"),
    path('confirm/<str:pk>/', views.confirm, name="ConfirmEmail"),
    path('unsubscribe/<str:pk>/', views.unsubscribe, name="Unsubscribe"),
    path('snooze/<str:pk>/', views.snooze, name="Snooze"),
    path('resume/<str:pk>/', views.resume, name="Resume"),
    path('send_question/', views.send_question, name="send"),
]