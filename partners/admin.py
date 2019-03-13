from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from partners.resources import PartnersResources


class PartnersAdmin(ImportExportActionModelAdmin):
    fields = (
        "bms_user", "name", "code", "reporting_period", "mode", "region",
        "materials", "sponsorship", "activities", "propaganda", "note"
    )
    list_per_page = 30
    list_display = (
        "bms_user", "name", "reporting_period", "mode", "region", "materials",
        "sponsorship", "activities", "propaganda"
    )
    list_display_links = ('bms_user', 'name')
    list_filter = ("mode", "region")
    radio_fields = {"mode": admin.HORIZONTAL, "region": admin.HORIZONTAL}
    save_as_continue = False
    search_fields = ("bms_user__username", )
    resource_class = PartnersResources


# class PropagandaAdmin(admin.ModelAdmin):
#     autocomplete_fields = ("partner", "bms_user")
#     fields = ("partner", "date", "bms_user",)
#     list_per_page = 30
#     list_display = ("partner", "date", "bms_user",)
#     list_display_links = ('bms_user', )
#     save_as_continue = False
#     search_fields = ("bms_user__username", "partner__name")
