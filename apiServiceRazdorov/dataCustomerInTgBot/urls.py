from django.urls import path, include
from .views import GetCurrentClient, NewClient, GetClient, InfoGetClient, LinkGetClient, UserGetMoney

urlpatterns = [
    path('', GetCurrentClient.as_view()),
    path('new-client/', NewClient.as_view()),
    path('get-client/', GetClient.as_view()),
    path('info-client/get/', InfoGetClient.as_view()),
    path('info-client/get-link/', LinkGetClient.as_view()),
    path('info-client/get-money/', UserGetMoney.as_view()),
]
