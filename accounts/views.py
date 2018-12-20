from django.shortcuts import render


def index(request):
    """
    The entrance of Colobaby-Recruiting Project
    """
    template_name = "accounts/index.html"
    extra_context = {
        'page_title': "结直肠癌风险评估系统"
    }
    return render(request, template_name, extra_context)


def register(request):
    """
    The entrance of Colobaby-Recruiting Project
    """
    template_name = "accounts/register.html"
    extra_context = {
        'page_title': "登陆",
    }
    return render(request, template_name, extra_context)
