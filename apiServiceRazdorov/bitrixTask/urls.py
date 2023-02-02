from django.urls import path, include
from .views import TaskAPIView

urlpatterns = [
    path('', TaskAPIView.as_view()),
]
