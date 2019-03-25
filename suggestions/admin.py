import os
import subprocess

from django.contrib import admin
from django.contrib.auth.tokens import default_token_generator
from django.urls import path, reverse

from bms_colowell.mixins import NotificationMixin
from bms_colowell.settings import DINGTALK_APPKEY, DINGTALK_SECRET,\
    DINGTALK_AGENT_ID, MEDIA_ROOT
from bms_colowell.utils import ScoreEvaluation, limit_suggestions
from suggestions.forms import CollectionsForm
from suggestions.models import Choices


class CollectionsAdmin(admin.ModelAdmin, NotificationMixin):
    """The suggestions mapping and the scoring for sample."""
    
    actions = ["generate_pdf"]
    appkey = DINGTALK_APPKEY
    appsecret = DINGTALK_SECRET
    fieldsets = (
        (None, {
            'fields': ('product', 'version', '_f10', '_f12', '_f08', '_f09', ),
        }),
        ('问卷答案', {
            'fields': (
                '_f01', '_f02', '_f11', '_f03', '_f04',
                '_f05', '_f06', '_f07',
            )
        }),
        ('健康管理', {
            'fields': ('t01', 't02', 't03', 't04', 't05', 't06', 't07',)
        }),
        ('高通量打分', {
            'fields': (
                'kras_mutation_rate', 'bmp3_mutation_rate',
                'ndrg4_mutation_rate', 'hemoglobin_content', 'score',
            )
        }),
        ('提交状态', {'fields': ('is_submit', )}),
    )
    form = CollectionsForm
    list_display = (
        'product', '_f01', '_f02', '_f03', '_f04', 'f05_string', 'f06_string',
        'f07_string', '_f08', '_f09', '_f10', 'is_submit', 'report_download'
    )
    list_filter = ('is_submit', )
    ordering = ('product__barcode', )
    radio_fields = {
        '_f01': admin.HORIZONTAL, '_f02': admin.HORIZONTAL,
        '_f03': admin.HORIZONTAL, '_f04': admin.HORIZONTAL,
        '_f08': admin.HORIZONTAL, '_f09': admin.HORIZONTAL,
        '_f10': admin.HORIZONTAL, '_f11': admin.HORIZONTAL,
        '_f12': admin.HORIZONTAL,
    }
    search_fields = ('product__barcode', )

    def f05_string(self, obj):
        return "；".join([f05.name for f05 in obj._f05.all()])
    f05_string.short_description = "下消化道症状"

    def f06_string(self, obj):
        return "；".join([f06.name for f06 in obj._f06.all()])
    f06_string.short_description = "其它病史"

    def f07_string(self, obj):
        return "；".join([f07.name for f07 in obj._f07.all()])
    f07_string.short_description = "慢性病史"

    def get_report(self, request, obj, token):
        """Method to generate pdf file."""
        
        # Generate pdf file by execute command line using wkhtmltopdf
        barcode = obj.product.barcode
        kwargs = {
            "barcode": barcode, "token": token, "user_id": request.user.id,
        }
        url = reverse("suggestions:report", kwargs=kwargs)
        input = "{}://{}{}".format(request.scheme, request.get_host(), url)
        output = os.path.join(MEDIA_ROOT, "reports/{}.pdf".format(barcode))
        command = [
            "wkhtmltopdf", "-q", "--disable-smart-shrinking",
            "-L", "0mm", "-R", "0mm", "-T", "0mm", "-B", "0mm"
        ]
        command.extend([input, output])

        # TODO: to update such a TERRIBLE version to task queue Celery
        get_pdf = subprocess.Popen(command)
        get_pdf.wait()
        
        # save pdf report to the corresponding model instance
        obj.download_url = input
        obj.pdf_upload = "reports/{}.pdf".format(barcode)
        obj.save()

    def generate_pdf(self, request, queryset):
        token = default_token_generator.make_token(request.user)
        import time
        start = time.time()
        for obj in queryset:
            self.get_report(request, obj, token)
        delta = time.time() - start
        self.message_user(request, "已成功生成报告，耗时{}".format(delta))
    generate_pdf.short_description = "生成PDF报告"
    
    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = (
            'product',
            '_f01', '_f02', '_f03', '_f04', '_f05', '_f06', '_f07', '_f08',
            '_f09', '_f10', '_f11', '_f12',
            't01', 't02', 't03', 't04', 't05', 't06', 't07',
            'kras_mutation_rate', 'bmp3_mutation_rate',
            'ndrg4_mutation_rate', 'hemoglobin_content', 'score',
            'is_submit',
        ) if obj and obj.is_submit else ()
        return self.readonly_fields
    
    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        
        initial = context["adminform"].form.initial
        if obj is not None and not obj.is_submit:
            for code in ["t01", "t02", "t03", "t04", "t05", "t06", "t07"]:
                initial[code] = limit_suggestions(obj, code=code)
            
        if obj and obj.f10 and obj.f12 and not obj.is_submit:
            mapping = {
                "f10c01": "LOW_RISK",
                "f10c02": "HIGH_RISK",
                "f12c01": "NEGATIVE",
                "f12c02": "WEAK_POSITIVE",
                "f12c03": "POSITIVE",
            }
            result = ScoreEvaluation(
                risk_state=mapping[obj.f10], hemoglobin_state=mapping[obj.f12]
            )
            kras_mutation_rate = round(result.kras_mutation_rate * 100, 2)
            bmp3_mutation_rate = round(result.bmp3_mutation_rate * 100, 2)
            ndrg4_mutation_rate = round(result.ndrg4_mutation_rate * 100, 2)
            hemoglobin_content = round(result.hemoglobin_content, 2)
            initial["kras_mutation_rate"] = kras_mutation_rate
            initial["bmp3_mutation_rate"] = bmp3_mutation_rate
            initial["ndrg4_mutation_rate"] = ndrg4_mutation_rate
            initial["hemoglobin_content"] = hemoglobin_content
            initial["score"] = result.score
        if obj and obj.is_submit:
            context['show_save'] = False
            context['show_delete'] = False
            context['show_save_and_continue'] = False
        return super().render_change_form(
            request, context, add=add, change=change, form_url=form_url,
            obj=obj
        )
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj and obj.is_submit:
            content = "{}已提交样本{}的健康管理数据".format(
                request.user.username, obj.product.barcode,
            )
            # recipients = ",".join(["091104142937895458", "06291639227812"])
            recipients = ",".join(["06291639227812"])
            self.send_work_notice(content, DINGTALK_AGENT_ID, recipients)
            call_back = self.send_dingtalk_result
            message = "已钉钉通知测试管理员" if call_back else "钉钉通知失败"
            self.message_user(request, message)
        else:
            self.message_user(request, "记录已保存，请及时跟进")


class ChoicesInline(admin.TabularInline):
    model = Choices
    extra = 0
    fields = ('code', 'name', )
    show_change_link = False


class FactorsAdmin(admin.ModelAdmin):
    fields = ('code', 'name', )
    list_display = ('code', 'name', )
    inlines = [ChoicesInline]
    ordering = ['code']


class TypesAdmin(admin.ModelAdmin):
    fields = ('code', 'name', )
    list_display = ('code', 'name', )
    ordering = ['code']


class VersionsAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', )
    ordering = ['code']
    fieldsets = (
        (None, {'fields': ('code', 'name', )}),
        ('字数限制', {
            'fields': (
                ('t01_length_min', 't01_length_max'),
                ('t02_length_min', 't02_length_max'),
                ('t03_length_min', 't03_length_max'),
                ('t04_length_min', 't04_length_max'),
                ('t05_length_min', 't05_length_max'),
                ('t06_length_min', 't06_length_max'),
                ('t07_length_min', 't07_length_max'),
            )
        }), ('图片上传', {
            'fields': (
                'reviewer', 'auditor', 'tester', 'disclaimer', 'signature',
            )
        }),
    )


class SuggestionsAdmin(admin.ModelAdmin):
    fields = (
        'code', 'type_name', 'factors', 'available_choices', 'connections',
        'expressions',
    )
    list_display = (
        'code', 'type_name', 'related_factors', 'related_choices',
        'expressions',
    )
    # filter_horizontal = ('factors', )
    readonly_fields = ('available_choices', )
    ordering = ['code']
    
    def related_factors(self, obj):
        return "\n".join([factor.code for factor in obj.factors.all()])
    related_factors.short_description = "建议关联因子"

    def related_choices(self, obj):
        if obj.connections is not None:
            strings = obj.connections.split(";")
        else:
            strings = ""
        return "\n".join(strings)
    related_choices.short_description = "建议关联选项"

    def available_choices(self, obj):
        available_factor_codes = [factor.code for factor in obj.factors.all()]
        available_choices = []
        for code in available_factor_codes:
            choices = Choices.objects.filter(factor__code=code)
            code_name = ["{}→👉→{}【{}】".format(
                c.code, c.name, c.factor.name
            ) for c in choices]
            available_choices.extend(code_name)
        return "\n".join(available_choices)
    available_choices.short_description = "可供选择的选项"
