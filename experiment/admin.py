from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportActionModelAdmin

'''
    提取管理
'''
class ExtExecuteAdmin(ImportExportActionModelAdmin):

    list_per_page = 50

    search_fields = ("status", "ext_date")

    save_on_top = False


'''
    质检管理
'''
class Quality_TestAdmin(ImportExportActionModelAdmin):

    list_per_page = 50

    search_fields = ("status", "ext_date")

    save_on_top = False

'''
    BS管理
'''
class BsTaskAdmin(ImportExportActionModelAdmin):

    list_per_page = 50

    search_fields = ("status", "ext_date")

    save_on_top = False

'''
    荧光定量管理
'''
class FluorescencequantificationAdmin(ImportExportActionModelAdmin):

    list_per_page = 50

    search_fields = ("status", "ext_date")

    save_on_top = False
