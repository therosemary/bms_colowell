from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from dingtalk_sdk_gmdzy2010.user_request import DeptUserRequest

from bms_colowell.mixins import NotificationMixin
from bms_colowell.settings import DINGTALK_APPKEY, DINGTALK_SECRET,\
    DINGTALK_AGENT_ID
from bms_colowell.utils import get_token, get_department_users


class BmsUserAdmin(UserAdmin):
    fieldsets = (
        ('账号密码', {
            'fields': ('username', ('last_name', 'first_name'), 'password')
        }), ('重要时间', {
            'fields': ('last_login', 'date_joined')
        }), ('用户信息', {
            'fields': ('mobile_phone', 'email', )
        }), ('用户权限', {
            'fields': (
                ('is_active', 'is_staff', 'is_superuser', 'is_bound', ),
                'groups', 'user_permissions',
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = (
        'username', 'mobile_phone', 'email', 'is_active', 'is_staff',
        'is_superuser', 'last_name', 'first_name', 'is_bound',
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = (
        'mobile_phone', 'username', 'first_name', 'last_name', 'email',
    )
    ordering = ('username', )
    filter_horizontal = ('groups', 'user_permissions', )


class WechatInfoAdmin(admin.ModelAdmin):
    fields = (
        "bms_user", "openid", "nickname", "sex", "city", "province", "country",
        "headimgurl", "unionid",
    )
    list_per_page = 30
    list_display = (
        "bms_user", "openid", "nickname", "sex", "city", "province", "country",
        "headimgurl", "unionid",
    )
    list_display_links = ('bms_user', )
    list_filter = ("sex", )
    save_as_continue = False
    search_fields = ("bms_user__username", )


class DingtalkInfoAdmin(admin.ModelAdmin, NotificationMixin):
    appkey = DINGTALK_APPKEY
    appsecret = DINGTALK_SECRET
    actions = [
        'bind_dingtalk_id', 'sync_dingtalk_info', 'test_work_notice',
    ]
    fields = (
        "bms_user", "userid", "name", "position", "jobnumber", "sex", "avatar",
        "unionid",
    )
    list_per_page = 30
    list_display = (
        "bms_user", "userid", "name", "position", "jobnumber", "sex", "avatar",
        "unionid",
    )
    list_display_links = ('bms_user', )
    list_filter = ("sex", )
    save_as_continue = False
    search_fields = ("bms_user__username", )
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser and "delete_selected" in actions:
            actions.pop("delete_selected")
            actions.pop('get_dingtalk_id')
            actions.pop('sync_dingtalk_info')
            actions.pop('test_work_notice')
        return actions

    def bind_dingtalk_id(self, request, queryset):
        params = {"appkey": self.appkey, "appsecret": self.appsecret}
        access_token = get_token(**params)
        users = get_department_users(access_token=access_token,
                                     department_name="医学事业部")
        for obj in queryset:
            for user in users:
                if obj.bms_user.username == user["name"]:
                    obj.userid = user["userid"]
                    obj.bms_user.is_bound = True
                    obj.bms_user.save()
                    obj.save()
                    break
        self.message_user(request, "已成功绑定钉钉帐户")
    bind_dingtalk_id.short_description = "【钉钉】绑定钉钉帐户"

    def sync_dingtalk_info(self, request, queryset):
        params = {"appkey": self.appkey, "appsecret": self.appsecret}
        access_token = get_token(**params)
        for obj in queryset:
            if obj.userid:
                params = {"access_token": access_token, "userid": obj.userid}
                userinfo = DeptUserRequest(params=params)
                userinfo.get_json_response()
                response = userinfo.json_response
                obj.name = response.get("name", "")
                obj.position = response.get("position", "")
                obj.jobnumber = response.get("jobnumber", "")
                obj.avatar = response.get("avatar", "")
                obj.unionid = response.get("unionid", "")
                obj.bms_user.mobile_phone = response.get("mobile", "")
                obj.bms_user.email = response.get("email", "")
                obj.bms_user.save()
                obj.save()
        self.message_user(request, "已成功同步选中的用户钉钉信息")
    sync_dingtalk_info.short_description = "【钉钉】同步钉钉信息"

    def test_work_notice(self, request, queryset):
        recipients = ",".join([obj.userid for obj in queryset])
        self.send_work_notice(
            "【医学BMS系统】测试消息", DINGTALK_AGENT_ID, recipients
        )
        call_back = self.send_dingtalk_result
        message = "已钉钉通知" if call_back else "钉钉通知失败"
        self.message_user(request, message)
    test_work_notice.short_description = "【钉钉】工作通知测试"


class DingtalkChatAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = (
        "name", "chat_id", "owner", "create_at", "is_valid"
    )
    list_display_links = ("name", )
    search_fields = ("chat_id", "name", )
    list_filter = ("is_valid", )
    fields = (
        "name", "chat_id", "owner", "members", "is_valid",
    )

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = (
            "name", "chat_id", "owner", "create_at", "is_valid"
        ) if not request.user.is_superuser else ()
        return self.readonly_fields

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial["owner"] = request.user.id
        initial["members"] = [request.user.id, ]
        return initial


class ChatTemplatesAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = (
        "name", "sign", "text", "link", "create_at", "is_valid"
    )
    list_display_links = ("name", )
    search_fields = ("name", "sign", "text", )
    list_filter = ("is_valid", "sign")
