from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.template.response import HttpResponse, TemplateResponse

from accounts.models import BmsUser
from lz_products.models import LzProducts


def lz_report_view(request, user_id=None, barcode=None, token=None):
    """View to generate specified report."""
    
    user = get_object_or_404(BmsUser, pk=user_id)
    if authenticate(request, user=user, token=token):
        report_context = {}
        try:
            lz_product = LzProducts.objects.get(barcode__exact=barcode)
        except LzProducts.DoesNotExist:
            return HttpResponse("不存在编号为{}的样品".format(barcode))
        
        report_context["barcode"] = lz_product.barcode
        report_context["sample_code"] = lz_product.sample_code
        report_context["risk_state"] = lz_product.risk_state
        report_context["received_date"] = lz_product.received_date
        report_context["test_date"] = lz_product.test_date
        report_context["report_date"] = lz_product.report_date
        
        template = "lz_report/lz_report.html"
        return TemplateResponse(request, template, report_context)
    else:
        return HttpResponse("授权失败")
