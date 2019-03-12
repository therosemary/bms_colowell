from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from bms_colowell.settings import DINGTALK_APPKEY, DINGTALK_SECRET,\
    DINGTALK_AGENT_ID
from bms_colowell.notice_mixin import NotificationMixin
from accounts.utils import get_token, get_sub_department_users
from dingtalk_sdk_gmdzy2010.user_request import DeptUserRequest


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
                ('is_active', 'is_staff', 'is_superuser'),
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
        'is_superuser', 'last_name', 'first_name',
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
        'get_dingtalk_id', 'sync_dingtalk_info',
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
    
    def get_dingtalk_id(self, request, queryset):
        params = {"appkey": self.appkey, "appsecret": self.appsecret}
        access_token = get_token(**params)
        users = get_sub_department_users(access_token=access_token,
                                         dept_name="医学事业部")
        for obj in queryset:
            for user in users:
                if obj.bms_user.username == user["name"]:
                    obj.userid = user["userid"]
                    obj.save()
        self.message_user(request, "同步选中的用户钉钉ID")
    get_dingtalk_id.short_description = "同步选中的用户钉钉ID"

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
    sync_dingtalk_info.short_description = "同步选中的用户钉钉信息"


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
        initial["chat_id"] = "12345678"
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
