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


class PartnerAdmin(admin.ModelAdmin):
    autocomplete_fields = ("partner", )
    fields = (
        "partner", "store_code", "store_name", "store_note",
    )
    list_per_page = 30
    list_display = (
        "partner", "store_code", "store_name", "created_at", "altered_at",
        "store_note",
    )
    list_display_links = ('partner', )
    save_as_continue = False
    search_fields = ("partner__username", )


class WechatInfoAdmin(admin.ModelAdmin):
    autocomplete_fields = ("bms_user", )
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
    autocomplete_fields = ("bms_user", )
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
