from django.contrib import admin
import re



class IntentionAdmin(admin.ModelAdmin):
    fields = ('intention_client', 'contact_number', 'items')
    list_display = ('intention_client', 'contact_number', 'items', 'fill_name',
                    'fill_date')
    list_per_page = 40
    save_as_continue = False
    date_hierarchy = 'fill_date'

    # def save_model(self, request, obj, form, change):
    #     if change:
    #         super(IntentionAdmin, self).save_model(request, obj, form, change)
    #     else:
    #         obj.fill_name = re.search(r'[^【].*[^】]', str(request.user))[0]
    #         obj.save()
