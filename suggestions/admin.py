import random
from django.contrib import admin
from suggestions.forms import CollectionsForm
from suggestions.utilities import ScoreEvaluation, mapping_suggestions
from suggestions.models import Choices


class CollectionsAdmin(admin.ModelAdmin):
    """The suggestions mapping and the scoring for sample."""
    
    fieldsets = (
        (None, {'fields': ('product', 'f10', 'f12', 'f08', 'f09', )}),
        ('问卷答案', {
            'fields': (
                'f01', 'f02', 'f11', 'f03', 'f04', ('_f05', '_f06', '_f07'),
            )
        }),
        ('建议和打分', {
            'fields': (
                'suggestions', 'kras_mutation_rate',
                'bmp3_mutation_rate', 'ndrg4_mutation_rate',
                'hemoglobin_content', 'score',
            )
        }),
        ('提交状态', {'fields': ('is_submit', )}),
    )
    form = CollectionsForm
    list_display = (
        'product', 'f01', 'f02', 'f03', 'f04', 'f05_string', 'f06_string',
        'f07_string', 'f08', 'f09', 'f10', 'is_submit',
    )
    list_filter = ('is_submit', )
    ordering = ('product__barcode', )
    radio_fields = {
        'f01': admin.HORIZONTAL, 'f02': admin.HORIZONTAL,
        'f03': admin.HORIZONTAL, 'f04': admin.HORIZONTAL,
        'f08': admin.HORIZONTAL, 'f09': admin.HORIZONTAL,
        'f10': admin.HORIZONTAL, 'f11': admin.HORIZONTAL,
        'f12': admin.HORIZONTAL,
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
    
    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = (
            'product', 'f01', 'f02', 'f03', 'f04', '_f05', '_f06', '_f07',
            'f08', 'f09', 'f10', 'f11', 'f12', 'kras_mutation_rate',
            'bmp3_mutation_rate', 'ndrg4_mutation_rate', 'hemoglobin_content',
            'score', 'suggestions', 'is_submit',
        ) if obj and obj.is_submit else ()
        return self.readonly_fields
    
    def render_change_form(self, request, context, add=False, change=False,
                           form_url='', obj=None):
        
        # Setting the initial data for decreasing the times of input
        initial = context["adminform"].form.initial
        
        if obj is not None:
            # food = random.sample(mapping_suggestions(obj, code="t02"), 4)
            # life = random.sample(mapping_suggestions(obj, code="t01"), 4)
            life = "\n\n".join(mapping_suggestions(obj, code="t01"))
            initial["suggestions"] = life
        if obj and obj.f10 and obj.f12:
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
            initial["kras_mutation_rate"] = result.kras_mutation_rate
            initial["bmp3_mutation_rate"] = result.bmp3_mutation_rate
            initial["ndrg4_mutation_rate"] = result.ndrg4_mutation_rate
            initial["hemoglobin_content"] = result.hemoglobin_content
            initial["score"] = result.score
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
    ordering = ['code']


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
    ordering = ['code']
    
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
