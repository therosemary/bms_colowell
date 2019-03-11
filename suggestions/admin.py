from django.contrib import admin
from suggestions.forms import CollectionsForm
from suggestions.utils import ScoreEvaluation, limit_suggestions
from suggestions.models import Choices


class CollectionsAdmin(admin.ModelAdmin):
    """The suggestions mapping and the scoring for sample."""
    
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
        'f07_string', '_f08', '_f09', '_f10', 'is_submit',
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
        if obj is not None:
            for code in ["t01", "t02", "t03", "t04", "t05", "t06", "t07"]:
                initial[code] = limit_suggestions(obj, code=code)
            
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
