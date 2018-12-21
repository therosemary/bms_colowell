from django.contrib.admin import AdminSite
from django.contrib.auth.admin import Group, GroupAdmin
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy
from django.views.decorators.cache import never_cache
from urllib import parse
from bms_colowell.settings import DINGTALK_APPID

from accounts.admin import BmsUserAdmin, WechatInfoAdmin, DingtalkInfoAdmin
from accounts.models import BmsUser, WechatInfo, DingtalkInfo
from partners.admin import PartnersAdmin, PropagandaAdmin
from partners.models import Partners, Propaganda
from products.admin import ProductsAdmin
from products.models import Products


class BMSAdminSite(AdminSite):
    site_title = "锐翌医学BMS系统"
    site_header = ugettext_lazy('后台管理')
    login_template = "admin/login.html"

    @never_cache
    def index(self, request, extra_context=None):
        """
        Displays the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
        app_list = self.get_app_list(request)
        context = dict(
            self.each_context(request),
            title=self.index_title,
            app_list=app_list,
        )
        context.update(extra_context or {})
        request.current_app = self.name
        return TemplateResponse(
            request, self.index_template or 'admin/index.html', context
        )

    @never_cache
    def login(self, request, extra_context=None):
        extra_context = extra_context or {}
        url = "http://{}/dingtalk_auth/".format(request.META["HTTP_HOST"])
        redirect_uri = parse.quote(url)
        params = {
            "appid": DINGTALK_APPID,
            "response_type": "code",
            "scope": "snsapi_login",
            "state": "test",
            "redirect_uri": redirect_uri,
        }
        uri_main = "https://oapi.dingtalk.com/connect/qrconnect"
        uri_params = "?appid={appid}&response_type={response_type}&" \
                     "scope={scope}&state={state}&" \
                     "redirect_uri={redirect_uri}".format(**params)
        dingtalk_qrcode_uri = "{}{}".format(uri_main, uri_params)
        extra_context["dingtalk_qrcode_uri"] = dingtalk_qrcode_uri
        return super().login(request, extra_context=extra_context)


BMS_admin_site = BMSAdminSite()
BMS_admin_site.register(Group, GroupAdmin)

BMS_admin_site.register(BmsUser, BmsUserAdmin)
BMS_admin_site.register(WechatInfo, WechatInfoAdmin)
BMS_admin_site.register(DingtalkInfo, DingtalkInfoAdmin)
BMS_admin_site.register(Partners, PartnersAdmin)
BMS_admin_site.register(Propaganda, PropagandaAdmin)
BMS_admin_site.register(Products, ProductsAdmin)
