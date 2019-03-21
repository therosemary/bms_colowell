import os

from django.contrib.auth import authenticate, get_user_model
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import HttpResponse, TemplateResponse

from lz_products.models import LzProducts, BatchDownloadRecords


BmsUserModel = get_user_model()


def file_iterator(file_name, chunk_size=512):
    with open(file_name, 'rb') as file_stream:
        while True:
            chunk = file_stream.read(chunk_size)
            if chunk:
                yield chunk
            else:
                break


def lz_report_view(request, user_id=None, barcode=None, token=None):
    """View to generate specified report."""
    
    user = get_object_or_404(BmsUserModel, pk=user_id)
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
        
        template = "report/lz_report.html"
        return TemplateResponse(request, template, report_context)
    else:
        return HttpResponse("授权失败")


def batch_download(request, user_id=None, serial_number=None, token=None):
    """View to response zipped files."""
    
    user = get_object_or_404(BmsUserModel, pk=user_id)
    if authenticate(request, user=user, token=token):
        record = get_object_or_404(BatchDownloadRecords, pk=serial_number)
        file_path = record.zipped_file.path
        file, content_type = file_iterator(file_path), 'application/zip'
        response = StreamingHttpResponse(file, content_type=content_type)
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
            "{}.zip".format(serial_number)
        )
        return response
    else:
        return HttpResponse("授权失败")
