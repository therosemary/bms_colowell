from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class BmsUserAdmin(UserAdmin):
    fieldsets = (
        ('账号密码', {
            'classes': ('collapse',),
            'fields': ('username', ('last_name', 'first_name'), 'password')
        }), ('重要时间', {
            'classes': ('collapse', 'wide'),
            'fields': ('last_login', 'date_joined')
        }), ('用户信息', {
            'fields': ('mobile_phone', 'email', )
        }), ('用户权限', {
            'classes': ('collapse', ),
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


class DingtalkInfoAdmin(admin.ModelAdmin):
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
