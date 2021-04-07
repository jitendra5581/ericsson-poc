from django.contrib import admin
from .models import *
from .forms import DeviceForm


class PrimaryInterfaceAdmin(admin.ModelAdmin):
    form = DeviceForm
    list_display = ('ip_address', 'device_type', 'username',
                    'enable_monitoring'
                    )
    class Meta:
        model = PrimaryInterface

admin.site.register(PrimaryInterface, PrimaryInterfaceAdmin)

class SecondaryInterfaceAdmin(admin.ModelAdmin):
    form = DeviceForm
    list_display = ('ip_address', 'get_primary', 'device_type', 'username',
                    'enable_monitoring'
                    )

    def get_primary(self, obj):
        return obj.get_primary_interface()  
    
    class Meta:
        model = SecondaryInterface

admin.site.register(SecondaryInterface, SecondaryInterfaceAdmin)
admin.site.site_header = 'Echelon Administration'