from django.shortcuts import render
from django.conf import settings
import difflib
import os
import datetime
import time
from django.http import HttpResponse

from .models import *
from utilities.switchlogs import *


def get_diff(file1 , file2):
    file1_path = file1
    file2_path = file2
    file1_contents = open(file1_path, 'r').readlines()
    file2_contents = open(file2_path, 'r').readlines()
    compare = difflib.unified_diff(file1_contents, file2_contents)
    deleted_records = list()
    added_records = list()
    for comp in compare:
        if(comp[0]=='-' and len(comp)>10):
            deleted_records.append(comp)
            print(comp)
        elif(comp[0]=='+' and len(comp)>10):
            added_records.append(comp)
            print(comp)
    return deleted_records, added_records, file1_contents, file2_contents

def scan_view(request):
    prim__device_qs = PrimaryInterface.objects.all()
    deleted_records = list()
    added_records = list()
    file1 =''
    file2 = ''
    primary_device_ip = ''
    sec_device_ip = ''

    if request.method == 'POST':
        primary_device_id = request.POST.get('primary_device')
        print('pid>>', primary_device_id)
        qs = PrimaryInterface.objects.filter(id=primary_device_id)

        #*********primary device details *****************
        primary_device_ip = qs.first().ip_address
        prim_device_type = qs.first().device_type
        prim_username = qs.first().username
        prim_password = qs.first().password
        prim_secret = qs.first().secret

        # ******************** logs scanner ***************
        log_obj = GenerateLogs()
        primary_log_file_path = log_obj.primary_log(prim_device_type, 
                                    primary_device_ip, prim_username,
                                    prim_password, prim_secret
                                    )

        qs2 = SecondaryInterface.objects.get(primary_interface__id=primary_device_id)

        #************ sec. device details **************
        sec_device_ip = qs2.ip_address
        sec_device_type = qs2.device_type
        sec_username = qs2.username
        sec_password = qs2.password
        sec_secret = qs2.secret

        sec_log_file_path = log_obj.secondary_log(sec_device_type, 
                                    sec_device_ip, sec_username, 
                                    sec_password, sec_secret
                                    )
        
        deleted_records, added_records, file1, file2 = get_diff(primary_log_file_path, 
                                                               sec_log_file_path
                                                               )
    context = {
        'device_objs' : prim__device_qs,
        'deleted_records': deleted_records,
        'added_records': added_records,
        'primary_device_logs' : file1,
        'secordary_device_logs' : file2,
        'primary_device_ip' : primary_device_ip,
        'sec_device_ip' : sec_device_ip
    }    
    return render(request, 'diffcheckerapp/diff.html', context)

def devices_view(request):
    qs = SecondaryInterface.objects.all()
    context = {
        'deveices_qs': qs
    }
    return render(request, 'diffcheckerapp/all_devices.html', context)

def scanner_view(request):
    time.sleep(10)
    return HttpResponse('done')
    
