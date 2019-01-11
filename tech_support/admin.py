from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from django.contrib.admin import ModelAdmin
from tech_support.models import *


class BoxesInline(admin.TabularInline):
    model = Boxes
    fields = ["bar_code", "name", "type", "projec_source", "is_danger"]

    def get_readonly_fields(self, request, obj=None):
        if obj.submit:
            self.readonly_fields = ["bar_code", "name", "type",
                                    "projec_source", "is_danger"]
        return self.readonly_fields


class BoxDeliveriesAdmin(ImportExportActionModelAdmin):
    """盒子发货管理"""
    inlines = [BoxesInline]
    list_per_page = 50
    search_fields = ("sale_man", "send_date")
    save_on_top = False
    list_display = ('index_number', "sale_man", "customer",
                    'send_number', 'send_date', 'made_date')
    list_display_links = ('index_number',)
    exclude = ["index_number", ]

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.submit:
                self.readonly_fields = ['sale_man', "customer", "box_number",
                                        "send_number", "send_date",
                                        'made_date', "submit"]
                return self.readonly_fields
        except AttributeError:
            return self.readonly_fields
        return self.readonly_fields

    """命名规则未定"""
    def save_model(self, request, obj, form, change):
        if not obj.index_number:
            obj.index_number = "A0000002"
        obj.save()

    # def save_formset(self, request, form, formset, change):
    #     instances = formset.save(commit=False)
    #     for obj in formset.deleted_objects:
    #         obj.delete()
    #     if instances:
    #         for instance in instances:
    #             if not instance.status and form.cleaned_data["submit"]:
    #                 instance.status = 1
    #             instance.save()
    #             formset.save_m2m()


class BoxesAdmin(ImportExportActionModelAdmin):
    """盒子管理"""
    list_per_page = 50
    search_fields = ("status", "report_date")
    save_on_top = False
    list_display = (
        'index_number', "bar_code", 'type', 'status',
        'report_date'
    )
    list_display_links = ('index_number',)


class ExtMethodAdmin(ModelAdmin):
    """提取方法管理"""
    list_display = ('method',)


class ExtSubmitAdmin(ImportExportActionModelAdmin):
    """提取下单管理"""
    list_per_page = 50
    save_on_top = False
    list_display = ("extsubmit_number", 'boxes', "exp_method",)
    list_display_links = ('extsubmit_number',)

    def get_readonly_fields(self, request, obj=None):
        try:
            if obj.submit:
                self.readonly_fields = ["extsubmit_number", 'boxes',
                                        "exp_method", "submit"]
                return self.readonly_fields
        except AttributeError:
            return self.readonly_fields
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not obj.extsubmit_number:
            obj.extsubmit_number = "EXT0000001"
        obj.save()