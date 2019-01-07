from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportActionModelAdmin
from experiment.models import *
'''
    提取管理
'''
class ExtExecuteAdmin(ImportExportActionModelAdmin):

    list_per_page = 50

    search_fields = ("status", "ext_date")

    save_on_top = False

    list_display = ('ext_number', "boxes","test_number", 'ext_method', 'ext_date', 'status')

    list_display_links = ('ext_number',)


'''
    质检管理
'''
class Quality_TestAdmin(ImportExportActionModelAdmin):

    list_per_page = 50

    search_fields = ("status", "qua_date")

    save_on_top = False

    list_display = ('qua_number', "boxes", 'test_number', 'operator', 'qua_date',"status")

    list_display_links = ('qua_number',)


'''
    BS管理
'''
class BsTaskAdmin(ImportExportActionModelAdmin):

    list_per_page = 50

    search_fields = ("status", "bs_date")

    save_on_top = False

    list_display = ('bs_number', "boxes", 'test_number',"bs_times", 'operator', 'bs_date', "status")

    list_display_links = ('bs_number',)


'''
    荧光定量管理
'''
class FluorescencequantificationAdmin(ImportExportActionModelAdmin):

    list_per_page = 50

    search_fields = ("status", "fq_date")

    save_on_top = False

    list_display = ('fq_number', "boxes", 'test_number', 'operator', 'fq_date', "status")

    list_display_links = ('fq_number',)


admin.site.register(ExtExecute,ExtExecuteAdmin)
admin.site.register(Quality_Test,Quality_TestAdmin)
admin.site.register(BsTask,BsTaskAdmin)
admin.site.register(Fluorescencequantification,FluorescencequantificationAdmin)