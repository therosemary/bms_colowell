from import_export.admin import ImportExportActionModelAdmin
from experiments.resources import ExperimentsResource


class ExperimentsAdmin(ImportExportActionModelAdmin):
    list_display = ("index_number", "receive_date", "ext_method")
    list_display_links = ("index_number", "ext_method")
    resource_class = ExperimentsResource
    fieldsets = (
        ('实验相关信息', {
            'fields': (
                'index_number', 'boxes', "receive_date",
                "projects_source")
        }),
        ('提取', {
            'fields': (
                ('ext_objective', "ext_method"),
                ("ext_start_number", "ext_hemoglobin"),
                ("ext_cz_volume", 'ext_density',),
                ("ext_elution_volume", 'produce_', "ext_qualified"),
                ("ext_operator", 'ext_date',), "ext_note",
                "submit_ext")
        }),
        ('质检', {
            'fields': (
                ('qua_test_number', "qua_instrument"),
                ("qua_sample_size", "qua_loop_number"),
                ("qua_background",),
                ("qua_noise", 'qua_ct', "qua_amplification_curve"),
                ("qua_is_quality",), ("qua_operator", "qua_date"),
                "qua_note", "submit_qua")
        }),
        ('BIS', {
            'fields': (
                ('bis_test_number', "bis_begin"),
                ("bis_template", "bis_elution"),
                ("bis_is_quality",),
                ("bis_date", 'bis_note'), "submit_bis")
        }),
        ('荧光定量', {
            'fields': (
                ('fq_test_number', "fq_instrument"),
                ("fq_loop_number", "fq_background"),
                ("fq_actb_noise", 'fq_actb_ct', "fq_actb_amp"),
                ("fq_sfrp2_noise", 'fq_sfrp2_ct', "fq_sfrp2_amp"),
                ("fq_sdc2_noise", 'fq_sdc2_ct', "fq_sdc2_amp"),
                ("fq_is_quality",), ("fq_operator", "fq_date"),
                "qualified_", "fq_suggest", "submit_fq")
        }),
    )
    # readonly_fields = ["produce_", "qualified_", "ext_qualified"]

    def produce_(self, obj):
        if obj:
            if obj.elution_volume and obj.ext_density:
                pro = float(obj.elution_volume) * float(obj.ext_density)
                return pro
            else:
                return None
        return None

    produce_.short_description = "提取-产出"

    def qualified_(self, obj):
        if obj:
            try:
                if float(obj.fq_actb_ct) <= 38.5:
                    return "合格"
                else:
                    return "不合格"
            except TypeError:
                return None
        return None

    produce_.short_description = "荧光定量-是否合格"

    def ext_qualified(self, obj):
        if obj:
            if obj.elution_volume and obj.ext_density:
                pro = float(obj.elution_volume) * float(obj.ext_density)
                if pro > 2:
                    return "是"
                else:
                    return "否"
            else:
                return None
        return None

    ext_qualified.short_description = "提取-是否合格"

    def get_readonly_fields(self, request, obj=None):
        if obj:
            readonly = ["produce_", "qualified_", "ext_qualified"]
            ext = ['ext_objective', "ext_method",
                   "ext_start_number", "ext_hemoglobin",
                   "ext_cz_volume", 'ext_density',
                   "ext_elution_volume", 'produce_', "ext_qualified",
                   "ext_operator", 'ext_date', "ext_note", "submit_ext"]
            qua = ['qua_test_number', "qua_instrument",
                   "qua_sample_size", "qua_loop_number",
                   "qua_background",
                   "qua_noise", 'qua_ct', "qua_amplification_curve",
                   "qua_is_quality", "qua_operator", "qua_date",
                   "qua_note", "submit_qua"]
            bis = ['bis_test_number', "bis_begin",
                   "bis_template", "bis_elution",
                   "bis_is_quality",
                   "bis_date", 'bis_note', "submit_bis"]
            fq = ['fq_test_number', "fq_instrument",
                  "fq_loop_number", "fq_background",
                  "fq_actb_noise", 'fq_actb_ct', "fq_actb_amp",
                  "fq_sfrp2_noise", 'fq_sfrp2_ct', "fq_sfrp2_amp",
                  "fq_sdc2_noise", 'fq_sdc2_ct', "fq_sdc2_amp",
                  "fq_is_quality", "fq_operator", "fq_date",
                  "qualified_", "fq_suggest", "submit_fq"]
            if obj.submit_ext:
                readonly.extend(ext)
            if obj.submit_qua:
                readonly.extend(qua)
            if obj.submit_bis:
                readonly.extend(bis)
            if obj.submit_fq:
                readonly.extend(fq)
            return readonly
        else:
            return ["produce_", "qualified_", "ext_qualified"]
