from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from django.contrib.admin import ModelAdmin
from tech_support.models import *
'''
    盒子发货管理
'''
class BoxDeliveriesAdmin(ImportExportActionModelAdmin):

    list_per_page = 50

    search_fields = ("sale_man", "send_date")

    save_on_top = False

    list_display = ('index_number', "sale_man","customer", 'send_number', 'send_date', 'made_date')

    list_display_links = ('index_number',)


'''
    盒子管理
'''
class BoxesAdmin(ImportExportActionModelAdmin):

    list_per_page = 50

    search_fields = ("status", "report_date")

    save_on_top = False

    list_display = ('index_number', "bar_code", 'type', 'status', 'report_date')

    list_display_links = ('index_number',)


'''
    提取方法管理
'''
class ExtMethodAdmin(ModelAdmin):


    list_display = ('method')



'''
    提取下单管理
'''
class ExtSubmitAdmin(ImportExportActionModelAdmin):

    list_per_page = 50

    # search_fields = ("",)

    save_on_top = False

    list_display = ("extsubmit_number",'boxes', "exp_method",)

    list_display_links = ('fq_number',)


admin.site.register(BoxDeliveries,BoxDeliveriesAdmin)
admin.site.register(Boxes,BoxesAdmin)
admin.site.register(ExtMethod,ExtMethodAdmin)
admin.site.register(ExtSubmit,ExtSubmitAdmin)