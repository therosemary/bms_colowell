from django.contrib import admin


class PartnersAdmin(admin.ModelAdmin):
    autocomplete_fields = ("bms_user", )
    fields = (
        "bms_user", "name", "code", "mode", "region", "materials",
        "sponsorship", "activities", "propaganda", "note"
    )
    list_per_page = 30
    list_display = (
        "bms_user", "name", "code", "mode", "region", "materials",
        "sponsorship", "activities", "propaganda", "note",
    )
    list_display_links = ('bms_user', )
    list_filter = ("mode", "region")
    radio_fields = {"mode": admin.HORIZONTAL, "region": admin.HORIZONTAL}
    save_as_continue = False
    search_fields = ("bms_user__username", )


# class PropagandaAdmin(admin.ModelAdmin):
#     autocomplete_fields = ("partner", "bms_user")
#     fields = ("partner", "date", "bms_user",)
#     list_per_page = 30
#     list_display = ("partner", "date", "bms_user",)
#     list_display_links = ('bms_user', )
#     save_as_continue = False
#     search_fields = ("bms_user__username", "partner__name")
