from django.urls import path
from .views import *


urlpatterns = [
    path('', scan_view),
    path('devices/', devices_view)
]
