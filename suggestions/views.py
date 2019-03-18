from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.template.response import HttpResponse, TemplateResponse

from accounts.models import BmsUser
from products.models import Products
from suggestions.models import Collections


def report_view(request, user_id=None, barcode=None, token=None):
    """View to generate specified report."""
    
    user = get_object_or_404(BmsUser, pk=user_id)
    if authenticate(request, user=user, token=token):
        report_context = {}
        try:
            product = Products.objects.get(barcode__exact=barcode)
            collection = Collections.objects.get(product_id__exact=barcode)
        except Products.DoesNotExist:
            return HttpResponse("不存在编号为{}的库存".format(barcode))
        except Collections.DoesNotExist:
            return HttpResponse("不存在编号为{}的报告".format(barcode))
        
        report_version = collection.version_id
        report_context["barcode"] = collection.product_id
        report_context["barcode_img"] = product.barcode_img.url
        
        # TODO: get userinfo from tech_support models
        report_context["gender"] = "男"
        report_context["birthday"] = "男"
        report_context["mobile_phone"] = "男"
        report_context["send_date"] = "男"
        
        # experiment data for this product
        mapping = {"f10c01": "低风险", "f10c02": "高风险"}
        report_context["risk_state"] = mapping.get(collection.f10, "")
        report_context["score"] = collection.score
        report_context["kras_mutation_rate"] = collection.kras_mutation_rate
        report_context["bmp3_mutation_rate"] = collection.bmp3_mutation_rate
        report_context["ndrg4_mutation_rate"] = collection.ndrg4_mutation_rate
        report_context["hemoglobin_content"] = collection.hemoglobin_content
        
        # images of reviewers group under current version
        report_context["reviewer"] = collection.version.reviewer.url
        report_context["auditor"] = collection.version.auditor.url
        report_context["tester"] = collection.version.tester.url
        report_context["signature"] = collection.version.signature.url
        
        # images of reviewers group under current version
        report_context["t01"] = collection.t01
        report_context["t02"] = collection.t02
        report_context["t03"] = collection.t03
        report_context["t04"] = collection.t04
        report_context["t05"] = collection.t05
        report_context["t06"] = collection.t06
        report_context["t07"] = collection.t07
        
        template = "report/{}.html".format(report_version)
        return TemplateResponse(request, template, report_context)
    else:
        return HttpResponse("授权失败")
