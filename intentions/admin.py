from import_export.admin import ImportExportActionModelAdmin
from intentions.resources import IntentionSource
from intentions.models import Intentions


class IntentionAdmin(ImportExportActionModelAdmin):
    """意向池信息管理"""
    fields = (
        'salesman', 'intention_client', 'contact_name', 'contact_number',
        'follow_situations', 'material_situations', 'other_situations',
        'remark',
    )
    list_display = (
        'salesman', 'intention_client', 'contact_name', 'contact_number',
        'follow_situations', 'material_situations', 'other_situations',
        'remark',
    )
    list_per_page = 40
    save_as_continue = False
    date_hierarchy = 'fill_date'
    resource_class = IntentionSource

    # def get_changeform_initial_data(self, request):
    #     initial = super(IntentionAdmin, self).get_changeform_initial_data(request)
    #     initial['fill_name'] = request.user
    #     return initial
