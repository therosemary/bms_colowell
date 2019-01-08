from django.contrib import admin
# import re
# from accounts.models import BmsUser


class IntentionAdmin(admin.ModelAdmin):
    """意向池信息管理"""
    fields = (
        'intention_client', 'contact_number', 'items'
    )
    list_display = (
        'intention_client', 'contact_number', 'items', 'fill_name', 'fill_date'
    )
    list_per_page = 40
    save_as_continue = False
    date_hierarchy = 'fill_date'

    # TODO：20190108 自动获取当前登录用户objects，关联填写人信息
    # def save_model(self, request, obj, form, change):
    #     if change:
    #         super(IntentionAdmin, self).save_model(request, obj, form, change)
    #     else:
    #         # user_name = re.search(r'[^【].*[^】]', str(request.user))[0]
    #         # obj.fill_name =
    #         # obj.fill_name =
    #         obj.save()
