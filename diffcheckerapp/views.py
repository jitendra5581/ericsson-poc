from django.shortcuts import render
from django.conf import settings
import difflib
import os
import datetime

from .models import *


def get_diff(file1 , file2):
    file1_path = os.path.join(settings.LOGS_URL, file1)
    file2_path = os.path.join(settings.LOGS_URL, file2)
    file1 = open(file1_path, 'r').readlines()
    file2 = open(file2_path, 'r').readlines()
    # compare = difflib.HtmlDiff().make_file(fromlines=file1, tolines=file2,
    #                                            fromdesc=(datetime.date.today() - datetime.timedelta(
    #                                                days=1)).isoformat(),
    #                                            todesc=datetime.date.today().isoformat())
    compare = difflib.unified_diff(file1, file2)
    deleted_records = list()
    added_records = list()
    for comp in compare:
        if(comp[0]=='-' and len(comp)>10):
            deleted_records.append(comp)
            print(comp)
        elif(comp[0]=='+' and len(comp)>10):
            added_records.append(comp)
            print(comp)

    # print(compare)
    return deleted_records, added_records, file1, file2

def scan_view(request):
    qs = PrimaryInterface.objects.all()
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
        primary_device_ip = qs.first().ip_address
        qs2 = SecondaryInterface.objects.get(primary_interface__id=primary_device_id)
        sec_device_ip = qs2.ip_address
        deleted_records, added_records, file1, file2 = get_diff('device1.text', 'device2.txt')
        
            
    context = {
        'device_objs' : qs,
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

