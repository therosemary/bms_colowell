import random
from django.contrib import admin
from suggestions.forms import CollectionsForm
from suggestions.utilities import ScoreEvaluation, mapping_suggestions
from suggestions.models import Choices, Factors, Suggestions


class CollectionsAdmin(admin.ModelAdmin):
    """合同信息管理"""
    fieldsets = (
        (None, {'fields': ('product', )}),
        ('检测结果', {'fields': ('f10', 'f12',)}),
        ('身体状态', {'fields': ('f08', 'f09',)}),
        ('问卷问题', {
            'fields': (
                'f01', 'f02', 'f11', 'f03', 'f04', ('_f05', '_f06', '_f07'),
            )
        }),
        ('提交状态', {
            'fields': (
                'suggestions', 'kras_mutation_rate',
                'bmp3_mutation_rate', 'ndrg4_mutation_rate',
                'hemoglobin_content', 'score', 'is_submit',
            )
        }),
    )
    form = CollectionsForm
    list_display = (
        'product', 'f01', 'f02', 'f03', 'f04', 'f05_string', 'f06_string',
        'f07_string', 'f08', 'f09', 'f10',
    )
    radio_fields = {
        'f01': admin.HORIZONTAL,
        'f02': admin.HORIZONTAL,
        'f03': admin.HORIZONTAL,
        'f04': admin.HORIZONTAL,
        'f08': admin.HORIZONTAL,
        'f09': admin.HORIZONTAL,
        'f10': admin.HORIZONTAL,
        'f11': admin.HORIZONTAL,
        'f12': admin.HORIZONTAL,
    }
    search_fields = ('product__barcode', )
    ordering = ('product__barcode', )

    def f05_string(self, obj):
        return "；".join([f05.name for f05 in obj._f05.all()])
    f05_string.short_description = "下消化道症状"

    def f06_string(self, obj):
        return "；".join([f06.name for f06 in obj._f06.all()])
    f06_string.short_description = "其它病史"

    def f07_string(self, obj):
        return "；".join([f07.name for f07 in obj._f07.all()])
    f07_string.short_description = "慢性病史"
    
    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = (
            'f01', 'f02', 'f03', 'f04', '_f05', '_f06', '_f07', 'f08',
            'kras_mutation_rate', 'bmp3_mutation_rate', 'ndrg4_mutation_rate',
            'hemoglobin_content', 'score', 'f09', 'f10', 'f11', 'f12',
            'suggestions', 'is_submit',
        ) if obj and obj.is_submit else ()
        return self.readonly_fields
    
    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        initial = context["adminform"].form.initial
        mapping = {
            "f10c01": "LOW_RISK",
            "f10c02": "HIGH_RISK",
            "f12c01": "NEGATIVE",
            "f12c02": "WEAK_POSITIVE",
            "f12c03": "POSITIVE",
        }
        if obj and obj.f10 and obj.f12:
            result = ScoreEvaluation(
                risk_state=mapping[obj.f10], hemoglobin_state=mapping[obj.f12]
            )
            initial["kras_mutation_rate"] = result.kras_mutation_rate
            initial["bmp3_mutation_rate"] = result.bmp3_mutation_rate
            initial["ndrg4_mutation_rate"] = result.ndrg4_mutation_rate
            initial["hemoglobin_content"] = result.hemoglobin_content
            initial["score"] = result.score
        # life = random.sample(mapping_suggestions(obj, code="t01"), 4)
        life_suggestions = "\n\n".join(mapping_suggestions(obj, code="t01"))
        initial["suggestions"] = life_suggestions
        if obj and obj.is_submit:
            context['show_save'] = False
            context['show_delete'] = False
            context['show_save_and_continue'] = False
        return super().render_change_form(
            request, context, add=add, change=change, form_url=form_url,
            obj=obj
        )


class ChoicesInline(admin.TabularInline):
    model = Choices
    extra = 0
    fields = ('code', 'name', )
    show_change_link = False


class FactorsAdmin(admin.ModelAdmin):
    fields = ('code', 'name', )
    list_display = ('code', 'name', )
    inlines = [ChoicesInline]


class SuggestionsAdmin(admin.ModelAdmin):
    fields = (
        'code', 'name', 'factors', 'available_choices', 'connections',
        'expressions',
    )
    list_display = (
        'code', 'name', 'related_factors', 'connections', 'expressions',
    )
    filter_horizontal = ('factors', )
    readonly_fields = ('available_choices', )
    
    def related_factors(self, obj):
        return "；".join([factor.code for factor in obj.factors.all()])
    related_factors.short_description = "建议关联因子"

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

