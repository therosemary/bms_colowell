from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from intentions.models import Intentions
# import re
# from accounts.models import BmsUser

class IntentionSource(resources.ModelResource):

    class Meta:
        model = Intentions
        fields = (
            'intention_id', 'intention_client', 'contact_number', 'items',
            'fill_name', 'fill_date'
        )
        export_order = (
            'intention_id', 'intention_client', 'contact_number', 'items',
            'fill_date', 'fill_name'
        )
        skip_unchanged = True

    def get_export_headers(self):
        export_headers = [u'编号', u'意向客户', u'联系电话', u'事项', u'填写日期',
                          '填写人',]
        return export_headers


class IntentionAdmin(ImportExportActionModelAdmin):
    """意向池信息管理"""
    fields = (
        'intention_client', 'contact_number', 'items', 'submit_flag',
    )
    list_display = (
        'intention_client', 'contact_number', 'items', 'fill_name',
        'fill_date', 'submit_flag'
    )
    list_per_page = 40
    save_as_continue = False
    date_hierarchy = 'fill_date'
    resource_class = IntentionSource

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.submit_flag:
                self.readonly_fields = (
                    'intention_client', 'contact_number', 'items',
                    'submit_flag',
                )
        return self.readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        intention = Intentions.objects.get(intention_id=object_id)
        self.get_readonly_fields(request, obj=intention)
        return super(IntentionAdmin, self).change_view(
            request, object_id, form_url='', extra_context=None
        )

    # TODO：20190108 自动获取当前登录用户objects，关联填写人信息
    # def save_model(self, request, obj, form, change):
    #     if change:
    #         super(IntentionAdmin, self).save_model(request, obj, form, change)
    #     else:
    #         # user_name = re.search(r'[^【].*[^】]', str(request.user))[0]
    #         # obj.fill_name =
    #         # obj.fill_name =
    #         obj.save()
