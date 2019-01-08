from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from django.contrib.admin import ModelAdmin
from tech_support.models import *

class BoxDeliveriesAdmin(ImportExportActionModelAdmin):
    '''盒子发货管理'''
    list_per_page = 50
    search_fields = ("sale_man", "send_date")
    save_on_top = False
    list_display = ('index_number', "sale_man", "customer",
                    'send_number', 'send_date', 'made_date')
    list_display_links = ('index_number',)



class BoxesAdmin(ImportExportActionModelAdmin):
    '''盒子管理'''
    list_per_page = 50
    search_fields = ("status", "report_date")
    save_on_top = False
    list_display = ('index_number', "bar_code", 'type', 'status'
                    , 'report_date')
    list_display_links = ('index_number',)



class ExtMethodAdmin(ModelAdmin):
    '''提取方法管理'''
    list_display = ('method',)


class ExtSubmitAdmin(ImportExportActionModelAdmin):
    '''提取下单管理'''
    list_per_page = 50
    save_on_top = False
    list_display = ("extsubmit_number",'boxes', "exp_method",)
    list_display_links = ('extsubmit_number',)


