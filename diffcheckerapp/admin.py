from django.contrib import admin, messages
from .models import *
from .forms import DeviceForm, CsvUploadForm
from django.urls import path
from django.shortcuts import render, redirect
import pandas as pd
from django.conf import settings
from datetime import datetime
import os
from django.utils.safestring import mark_safe
from django.http import HttpResponse



class PrimaryInterfaceAdmin(admin.ModelAdmin):
    change_list_template = "admin-templates/primary-inventory.html"
    form = DeviceForm
    list_display = ('ip_address', 'device_type', 'username',
                    'enable_monitoring'
                    )
    
    def get_urls(self):
        urls = super().get_urls()
        additional_urls = [
            path("upload-csv/", self.upload_csv),
            path("download-csv/", self.save_file)
        ]
        return additional_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra = extra_context or {}
        extra["csv_upload_form"] = CsvUploadForm()
        return super(PrimaryInterfaceAdmin, self).changelist_view(request, extra_context=extra)

    def upload_csv(self, request):
        if request.method == "POST":
            form = CsvUploadForm(request.POST, request.FILES)
            if(form.is_valid()):
                file_name = request.FILES['csv_file'].name
                if file_name.endswith('csv'):
                    df = pd.read_csv(request.FILES['csv_file'])
                    print(df)
                    devices = []
                    up_status = []
                    remarks = []
                    num_failed = 0
                    num_success = 0
                    for i in range(len(df)):
                        try:
                            prim_dev = PrimaryInterface(
                                ip_address=df.iloc[i][0],
                                device_type=df.iloc[i][1],
                                username=df.iloc[i][2],
                                password=df.iloc[i][3],
                                secret=df.iloc[i][4],
                                enable_monitoring=df.iloc[i][5]
                                )
                            prim_dev.save()
                            up_status.append('success')
                            remarks.append('')
                            num_success += 1 
                        except Exception as ex:
                            print(">>>>>>>>>>>>>>", str(ex))
                            if 'UNIQUE constraint failed' in str(ex):
                                print('ttttttttttttttttttt')
                                remarks.append('This Device details Already uploaded') 
                            else:
                                remarks.append('Details are not correct or invalid csv file')   
                            num_failed +=1
                            up_status.append('failed') 
                    file_name = 'pri'+'_'+str(datetime.now())+'_'+file_name
                    file_path = os.path.join(settings.CSV_URL,file_name)
                    # print('***********************')
                    df['upload_status'] = up_status
                    df['remarks'] = remarks
                    df.to_csv(path_or_buf=file_path)
                    d1 = 'Device'
                    d2 = 'Device'
                    if(num_success>1):
                        d1 = 'Devices'
                    if(num_failed>1):
                        d2 = 'Devices'    
                    msg = f"""{num_success} {d1} uploaded successfully and 
                    <span style='color:red'>{num_failed} {d2} failed </span>, 
                     <a href='download-csv?fn={file_name}'> click here </a> to download"""
                    messages.success(request, mark_safe(msg))
                 
                else:
                    messages.add_message(request, messages.ERROR, 'Only CSV file allowed here')
                    # print('Invalid file')    
        return redirect("..") 

    def save_file(self, request):
        file_name = request.GET.get('fn')
        data = open(os.path.join(settings.CSV_URL, file_name),'r').read()
        resp = HttpResponse(data, content_type='application/x-download')
        resp['Content-Disposition'] = f'attachment;filename={file_name}'
        return resp   

    class Meta:
        model = PrimaryInterface
admin.site.register(PrimaryInterface, PrimaryInterfaceAdmin)

class SecondaryInterfaceAdmin(admin.ModelAdmin):
    change_list_template = "admin-templates/primary-inventory.html"
    form = DeviceForm
    list_display = ('ip_address', 'get_primary', 'device_type', 'username',
                    'enable_monitoring'
                    )

    def get_primary(self, obj):
        return obj.get_primary_interface() 

    def get_urls(self):
        urls = super().get_urls()
        additional_urls = [
            path("upload-csv/", self.upload_csv),
            path("download-csv/", self.save_file)
        ]
        # print(additional_urls+urls)
        return additional_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra = extra_context or {}
        extra["csv_upload_form"] = CsvUploadForm()
        return super(SecondaryInterfaceAdmin, self).changelist_view(request, extra_context=extra)

    def upload_csv(self, request):
        if request.method == "POST":
            form = CsvUploadForm(request.POST, request.FILES)
            if(form.is_valid()):
                file_name = request.FILES['csv_file'].name
                if file_name.endswith('csv'):
                    df = pd.read_csv(request.FILES['csv_file'])
                    devices = []
                    up_status = []
                    remarks = []
                    num_failed = 0
                    num_success = 0

                    for i in range(len(df)):
                        
                        ip_address = ''
                        try:
                            primary_ip = df.iloc[i]['primary_device_ip_address']
                            obj_primary = PrimaryInterface.objects.get(ip_address=primary_ip)
                            if obj_primary:
                                sec_device = SecondaryInterface(
                                primary_interface=obj_primary,
                                ip_address=df.iloc[i]['secondary_device_ip_address'],
                                device_type=df.iloc[i]['device_type'],
                                username=df.iloc[i][2],
                                password=df.iloc[i]['password'],
                                secret=df.iloc[i]['secret'],
                                enable_monitoring=df.iloc[i]['enable']
                                )
                                sec_device.save() 
                            up_status.append('success')
                            remarks.append('')
                            num_success += 1    
                        except Exception as ex:
                            if 'does not exist' in str(ex):
                                remarks.append('Primary Device with this ip is not uploaded')
                            else:
                                remarks.append('Invalid column order or name or csv file')
                            up_status.append('failed')  
                             
                            num_failed +=1
                    file_name = str(datetime.now())+'_'+file_name
                    file_path = os.path.join(settings.CSV_URL,file_name)
                    # print('***********************')
                    df['upload_status'] = up_status
                    df['remarks'] = remarks
                    df.to_csv(path_or_buf=file_path)
                    d1 = 'Device'
                    d2 = 'Device'
                    if(num_success>1):
                        d1 = 'Devices'
                    if(num_failed>1):
                        d2 = 'Devices'    
                    msg = f"""{num_success} {d1} uploaded successfully and 
                    <span style='color:red'>{num_failed} {d2} failed </span>, 
                     <a href='download-csv?fn={file_name}'> click here </a> to download"""
                    messages.success(request, mark_safe(msg))
                else:
                    print('Invalid file')    
        return redirect("..")  

    def save_file(self, request):
        file_name = request.GET.get('fn')
        data = open(os.path.join(settings.CSV_URL, file_name),'r').read()
        resp = HttpResponse(data, content_type='application/x-download')
        resp['Content-Disposition'] = f'attachment;filename={file_name}'
        return resp    
            
    class Meta:
        model = SecondaryInterface

admin.site.register(SecondaryInterface, SecondaryInterfaceAdmin)
admin.site.site_header = 'Echelon Administration'