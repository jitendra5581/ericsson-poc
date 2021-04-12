from django.urls import path
from .views import *


urlpatterns = [
    # path('', scan_view),
    path('', single_device_scaner_view),
    path('devices/', devices_view),
    path('scanner/', scanner_view)
]
