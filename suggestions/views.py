from django.contrib.auth import authenticate
from django.template.response import HttpResponse, TemplateResponse
from accounts.models import BmsUser


def report_view(request, user_id=None, barcode=None, token=None):
    try:
        user = BmsUser.objects.get(pk=user_id)
    except BmsUser.DoesNotExist:
        return HttpResponse("不存在此用户")
    if authenticate(request, user=user, token=token):
        context = dict(username="test", barcode=barcode,)
        return TemplateResponse(request, "report/V01.html", context)
    else:
        return HttpResponse("授权失败")
