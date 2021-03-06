from django.db import models


class PrimaryInterface(models.Model):
    ip_address = models.CharField(max_length=100)
    device_type = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    secret = models.CharField(max_length=50)
    enable_monitoring = models.BooleanField()
    
    def __str__(self):
        return self.ip_address

    class Meta:
        verbose_name_plural = 'Primary Devices'

class SecondaryInterface(models.Model):
    primary_interface = models.OneToOneField(PrimaryInterface, 
                    on_delete=models.CASCADE, primary_key=True)
    ip_address = models.CharField(max_length=100)                
    device_type = models.CharField(max_length=100)
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    secret = models.CharField(max_length=50)
    enable_monitoring = models.BooleanField()

    def get_primary_interface(self):
        return self.primary_interface.ip_address
    
    class Meta:
        verbose_name_plural = 'Secondary Devices'



