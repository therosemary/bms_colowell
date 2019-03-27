from django.http import JsonResponse

from projects.models import ContractsInfo


# Create your views here.
def ajax_salesman(request):
    """动态获取当前合同对应的业务员"""
    print('111111111%s' % request.path)
    salesman_result = {'salesman': 'sale'}
    if request.is_ajax():
        contract_val = request.GET['contract_number']
        if contract_val is not None:
            contract_data = ContractsInfo.objects.get(contract_number=contract_val)
            # TODO: 业务员信息获取错误
            salesman_result = {'salesman': contract_data.staff_name}
    return JsonResponse(salesman_result)
    # return HttpResponse(json.dumps(salesman_result),
    # con   tent_type="application/json")
