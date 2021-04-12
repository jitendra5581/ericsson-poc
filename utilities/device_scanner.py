from netmiko import ConnectHandler
from django.conf import settings
import difflib
import os
import datetime


# commands************* 
# show ip interface brief
# show run interface f0/0
# show run 

class DeviceConfigScanner:

    #************ getting logs ******************
    
    def config_scanner(self, device_type, host, username, password, secret, interface_type):
        if(interface_type == 'primary_interface'):
            log_file_name = 'primary_'+host  
            log_file_path = os.path.join(settings.LOGS_URL, 'primary_logs/'+log_file_name)
        elif(interface_type == 'secondary_interface'):
            log_file_name = 'secondary_'+host  
            log_file_path = os.path.join(settings.LOGS_URL, 'secondary_logs/'+log_file_name)

        cisco_881 = {
            'device_type': device_type,
            'host':   host,
            'username': username,
            'password': password,
            "session_log": log_file_path,
            'secret': secret ,
        }
        net_connect = ConnectHandler(**cisco_881)
        enable = net_connect.enable()
        output = net_connect.send_command('show run interface f0/0')
        print(output)
        return log_file_path

    #******************comparing logs ************* 

    def get_difference(self, pri_log_file, sec_log_file):
        p_log_contents = open(pri_log_file, 'r').readlines()
        sec_log_contents = open(sec_log_file, 'r').readlines()
        compare = difflib.unified_diff(p_log_contents, sec_log_contents)
        deleted_conf = list()
        added_conf = list()
        for comp in compare:
            if(comp[0]=='-' and len(comp)>10):
                deleted_conf.append(comp)
                print(comp)
            elif(comp[0]=='+' and len(comp)>10):
                added_conf.append(comp)
                print(comp)

        return deleted_conf, added_conf, p_log_contents, sec_log_contents 

    def gen_report(self, deleted_conf, added_conf):
        log_file_name = 'primary_'+host  
        log_file_path = os.path.join(settings.LOGS_URL, 'primary_logs/'+log_file_name)
        
