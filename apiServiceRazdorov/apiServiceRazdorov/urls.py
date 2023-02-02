from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/bitrixTask/', include('bitrixTask.urls')),
    path('api/data_customer_in_tg/', include('dataCustomerInTgBot.urls')),
]
