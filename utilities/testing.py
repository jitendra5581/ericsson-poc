import difflib
import datetime
from netmiko import ConnectHandler
from django.conf import settings
import os


command = 'show running'

class GenerateLogs:
    primary_log_file_path = ''
    secondary_log_file_path = '' 
    def primary_log(self, device_type, ip_address, username, password, secret):
    # def primary_log(self, device_type, ip_address, username, secret):       
        session = ConnectHandler(
                                device_type=device_type, 
                                ip=ip_address, username=username,
                                password=password, secret=secret
                                )


        enable = session.enable()
        output = session.send_command(command)
        print("result>>>>>>>>>>", output)
    
obj = GenerateLogs()
obj.primary_log('cisco_ios', '10.10.10.2', 'admin', 'cisco', 'cisco')    