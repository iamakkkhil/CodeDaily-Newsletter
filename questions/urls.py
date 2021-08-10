from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.question, name="ReadQuestion"),
    path("display/<str:pk>/", views.displayQuestion, name="displayQuestion"),
    path("delete/<str:pk>/", views.deleteQuestion, name="deleteQuestion"),
    path("update/<str:pk>/", views.updateQuestion, name="updateQuestion"),
    path("add/", views.createQuestion , name="addQuestion"),
    path("report/<str:pk>/", views.reportQuestion , name="reportQuestion"),
]