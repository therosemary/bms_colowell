from import_export.admin import ImportExportActionModelAdmin
from intentions.resources import IntentionSource
from intentions.models import Intentions


class IntentionAdmin(ImportExportActionModelAdmin):
    """意向池信息管理"""

    # change_list_template = 'admin/intentions/intentions_change_list.html'
    fields = (
        'salesman', 'intention_client', 'contact_name', 'contact_number',
        'intention_progress', 'remark',
    )
    list_display = (
        'salesman', 'intention_client', 'contact_name', 'contact_number',
        'intention_progress', 'remark',
    )
    list_per_page = 40
    save_as_continue = False
    date_hierarchy = 'fill_date'
    list_display_links = ('salesman', 'intention_client')
    resource_class = IntentionSource

    def get_changeform_initial_data(self, request):
        initial = super(IntentionAdmin, self).get_changeform_initial_data(request)
        initial['salesman'] = request.user
        return initial
