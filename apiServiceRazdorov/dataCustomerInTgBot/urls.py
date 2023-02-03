from django.urls import path, include
from .views import GetCurrentClient, NewClient, GetClient, InfoGetClient

urlpatterns = [
    path('', GetCurrentClient.as_view()),
    path('new-client/', NewClient.as_view()),
    path('get-client/', GetClient.as_view()),
    path('info-client/get/', InfoGetClient.as_view()),

]
