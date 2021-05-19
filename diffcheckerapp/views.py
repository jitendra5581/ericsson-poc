from django.shortcuts import render
from django.conf import settings
import difflib
import os
import datetime
import time
from django.http import HttpResponse, JsonResponse
from .models import *
from utilities.switchlogs import *
from utilities.device_scanner import *


# def get_diff(file1 , file2):
#     file1_path = file1
#     file2_path = file2
#     file1_contents = open(file1_path, 'r').readlines()
#     file2_contents = open(file2_path, 'r').readlines()
#     compare = difflib.unified_diff(file1_contents, file2_contents)
#     deleted_records = list()
#     added_records = list()
#     for comp in compare:
#         if(comp[0]=='-' and len(comp)>10):
#             deleted_records.append(comp)
#             print(comp)
#         elif(comp[0]=='+' and len(comp)>10):
#             added_records.append(comp)
#             print(comp)
#     return deleted_records, added_records, file1_contents, file2_contents

# def scan_view(request):
#     prim__device_qs = PrimaryInterface.objects.all()
#     deleted_records = list()
#     added_records = list()
#     file1 =''
#     file2 = ''
#     primary_device_ip = ''
#     sec_device_ip = ''

#     if request.method == 'POST':
#         primary_device_id = request.POST.get('primary_device')
#         print('pid>>', primary_device_id)
#         qs = PrimaryInterface.objects.filter(id=primary_device_id)

#         #*********primary device details *****************
#         primary_device_ip = qs.first().ip_address
#         prim_device_type = qs.first().device_type
#         prim_username = qs.first().username
#         prim_password = qs.first().password
#         prim_secret = qs.first().secret

#         # ******************** logs scanner ***************
#         log_obj = GenerateLogs()
#         primary_log_file_path = log_obj.primary_log(prim_device_type, 
#                                     primary_device_ip, prim_username,
#                                     prim_password, prim_secret
#                                     )

#         qs2 = SecondaryInterface.objects.get(primary_interface__id=primary_device_id)

#         #************ sec. device details **************
#         sec_device_ip = qs2.ip_address
#         sec_device_type = qs2.device_type
#         sec_username = qs2.username
#         sec_password = qs2.password
#         sec_secret = qs2.secret

#         sec_log_file_path = log_obj.secondary_log(sec_device_type, 
#                                     sec_device_ip, sec_username, 
#                                     sec_password, sec_secret
#                                     )
        
#         deleted_records, added_records, file1, file2 = get_diff(primary_log_file_path, 
#                                                                sec_log_file_path
#                                                                )
#     context = {
#         'device_objs' : prim__device_qs,
#         'deleted_records': deleted_records,
#         'added_records': added_records,
#         'primary_device_logs' : file1,
#         'secordary_device_logs' : file2,
#         'primary_device_ip' : primary_device_ip,
#         'sec_device_ip' : sec_device_ip
#     }    
#     return render(request, 'diffcheckerapp/diff.html', context)

def devices_view(request):
    qs = SecondaryInterface.objects.all()
    context = {
        'deveices_qs': qs
    }
    return render(request, 'diffcheckerapp/all_devices.html', context)

def scanner_view(request):
    if request.is_ajax():
        primary_ip = request.GET.get('primary_ip')
        sec_ip = request.GET.get('secondary_ip')
        obj = DeviceConfigScanner()
        
        #****************primary device details ************
        pri_qs = PrimaryInterface.objects.get(ip_address=primary_ip)
        prim_device_type = pri_qs.device_type
        prim_username = pri_qs.username
        prim_password = pri_qs.password
        prim_secret = pri_qs.secret
        p_device_log_file_path = obj.config_scanner(prim_device_type,
                                     primary_ip, prim_username, 
                                     prim_password, prim_secret,
                                     'primary_interface')

        print('primary_log>>', p_device_log_file_path)                             
           
        #****************sec device details ************
        sec_qs = SecondaryInterface.objects.get(ip_address=sec_ip)
        sec_device_type = sec_qs.device_type
        sec_username = sec_qs.username
        sec_password = sec_qs.password
        sec_secret = sec_qs.secret
        sec_device_log_file_path = obj.config_scanner(sec_device_type,
                                     sec_ip, sec_username, sec_password, 
                                     sec_secret, 'secondary_interface')
        print('secondry_log>>>>>', sec_device_log_file_path)                             
        if (p_device_log_file_path and sec_device_log_file_path):
            del_conf, added_conf, p_log_cont, sec_log_cont = obj.get_difference(p_device_log_file_path, 
                                                               sec_device_log_file_path
                                                               )
            # print('log1>>>>', p_log_cont)
            # print('log2>>>>', sec_log_cont)
            result_dict = {
                'deleted_config': del_conf,
                'added_config': added_conf,
                'primary_log': p_log_cont,
                'secondary_log': sec_log_cont,
                'status': 'done',
                'primary_ip' : primary_ip,
                'secondary_ip' : sec_ip

            }
        else:
            result_dict = {
                'error':'Invalid ip or credetial details',
                'status': 'failed',
            }    
                   
    # time.sleep(5)
    return JsonResponse(result_dict)

def single_device_scaner_view(request):
    prim__device_qs = PrimaryInterface.objects.all()
    
    if request.is_ajax():
        primary_device_id = request.POST.get('primary_device')
        print('primary_device_id>>',primary_device_id)
        pri_qs = PrimaryInterface.objects.get(id=primary_device_id)
        obj = DeviceConfigScanner()
        #****************primary device details ************
        prim_device_type = pri_qs.device_type
        prim_device_ip = pri_qs.ip_address
        prim_username = pri_qs.username
        prim_password = pri_qs.password
        prim_secret = pri_qs.secret
        p_device_log_file_path = obj.config_scanner(prim_device_type,
                                     prim_device_ip, prim_username, 
                                     prim_password, prim_secret,
                                     'primary_interface'
                                     )

        print('primary_log>>', p_device_log_file_path)                             
           
        #****************sec device details ************
        sec_qs = SecondaryInterface.objects.get(primary_interface=pri_qs)
        sec_device_type = sec_qs.device_type
        sec_device_ip = sec_qs.ip_address        
        sec_username = sec_qs.username
        sec_password = sec_qs.password
        sec_secret = sec_qs.secret
        sec_device_log_file_path = obj.config_scanner(sec_device_type,
                                     sec_device_ip, sec_username, sec_password, 
                                     sec_secret, 'secondary_interface')
        print('sec device log path>>>>>>', sec_device_log_file_path)
        if(p_device_log_file_path and sec_device_log_file_path):
            del_conf, added_conf, p_log_cont, sec_log_cont = obj.get_difference(p_device_log_file_path, 
                                                              sec_device_log_file_path
                                                               )
            result_dict = {
                'deleted_config': del_conf,
                'added_config': added_conf,
                'primary_log': p_log_cont,
                'secondary_log': sec_log_cont,
                'status': 'done',
                'primary_ip' : prim_device_ip,
                'secondary_ip' : sec_device_ip
            }
            return JsonResponse(result_dict)
        else:
            result_dict = {
                'status': 'failed'
                }
            return JsonResponse(result_dict)


    context = {
            'device_objs' : prim__device_qs,
               } 

    return render(request, 'diffcheckerapp/diff-report.html', context)
    
