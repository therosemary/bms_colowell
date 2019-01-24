from import_export.admin import ImportExportActionModelAdmin
from intentions.resources import IntentionSource
from intentions.models import Intentions


class IntentionAdmin(ImportExportActionModelAdmin):
    """意向池信息管理"""
    fields = (
        'intention_client', 'contact_number', 'items', 'fill_name',
        'submit_flag',
    )
    list_display = (
        'intention_client', 'contact_number', 'items', 'fill_date',
        'fill_name', 'submit_flag'
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

    def get_changeform_initial_data(self, request):
        initial = super(IntentionAdmin, self).get_changeform_initial_data(request)
        initial['fill_name'] = request.user
        return initial
