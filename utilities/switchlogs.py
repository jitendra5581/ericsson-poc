import difflib
import datetime
from netmiko import ConnectHandler
from django.conf import settings
import os


command = 'show run interface f0/0'

class GenerateLogs:
    primary_log_file_path = ''
    secondary_log_file_path = '' 
    
    def primary_log(self, device_type, ip_address, username, password, secret):
        session = ConnectHandler(
                                device_type=device_type, 
                                ip=ip_address, username=username,
                                password=password, secret=secret
                                )

        enable = session.enable()
        output = session.send_command(command)
        log_file_path = os.path.join(settings.LOGS_URL, 'primary_logs')
        file_name = 'primary_'+ip_address+'_'+datetime.date.today().isoformat()
        self.primary_log_file_path = os.path.join(log_file_path,file_name)

        with open(self.primary_log_file_path, 'w') as primary_log:
            primary_log.write(output + '\n')
        primary_log.close() 
        return self.primary_log_file_path
    
    def secondary_log(self, device_type, ip_address, username, password, secret):
        session = ConnectHandler(
                                device_type=device_type, 
                                ip=ip_address, username=username,
                                password=password, secret=secret
                                )

        enable = session.enable()
        output = session.send_command(command)
        log_file_path = os.path.join(settings.LOGS_URL, 'secondary_logs')
        file_name = 'secondary_'+ip_address+'_'+datetime.date.today().isoformat()
        self.secondary_log_file_path = os.path.join(log_file_path,file_name)

        with open(self.secondary_log_file_path, 'w') as secondary_log:
            secondary_log.write(output + '\n')
        secondary_log.close()  
        return self.secondary_log_file_path



