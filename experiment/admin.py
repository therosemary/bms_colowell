from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin
from experiment.models import *


class ExtExecuteAdmin(ImportExportActionModelAdmin):
    """提取管理"""
    list_per_page = 50
    search_fields = ("status", "ext_date")
    save_on_top = False
    list_display = (
        'ext_number', "boxes", "test_number", 'ext_method', 'ext_date',
        'status',
    )
    list_display_links = ('ext_number',)
    filter_horizontal = ['boxes', ]


class QualityTestAdmin(ImportExportActionModelAdmin):
    """质检管理"""
    list_per_page = 50
    search_fields = ("status", "qua_date")
    save_on_top = False
    list_display = (
        'qua_number', "boxes", 'test_number', 'operator', 'qua_date',
        "status",
    )
    list_display_links = ('qua_number',)
    filter_horizontal = ['boxes', ]


class BsTaskAdmin(ImportExportActionModelAdmin):
    """BS管理"""
    list_per_page = 50
    search_fields = ("status", "bs_date")
    save_on_top = False
    list_display = (
        'bs_number', "boxes", 'test_number',"bs_times", 'operator', 'bs_date',
        "status",
    )
    list_display_links = ('bs_number',)
    filter_horizontal = ['boxes', ]


class FluorescenceQuantificationAdmin(ImportExportActionModelAdmin):
    """荧光定量管理"""
    list_per_page = 50
    search_fields = ("status", "fq_date")
    save_on_top = False
    list_display = (
        'fq_number', "boxes", 'test_number', 'operator', 'fq_date', "status",
    )
    list_display_links = ('fq_number',)
    filter_horizontal = ['boxes', ]


