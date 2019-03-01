from import_export import resources
from experiment.models import ExtExecute,QualityTest,\
    BsTask,FluorescenceQuantification


class ExtExecuteResource(resources.ModelResource):
    class Meta:
        model = ExtExecute
        skip_unchanged = True
        import_id_fields = ('ext_number',)
        fields = ('ext_number', 'operator',
                  'test_number', 'ext_method', "objective", 'start_number',
                  'hemoglobin', 'cizhutiji', 'ext_density', 'elution_volume',
                  "note")
        export_order = ('ext_number', 'operator',
                        'test_number', 'ext_method', "objective",
                        'start_number',
                        'hemoglobin', 'cizhutiji', 'ext_density',
                        'elution_volume',
                        "note")

    def get_export_headers(self):
        return ["ext_number", "操作人员", "试剂批号", "提取方法", "目的",
                "起始取样量(ml)", "血红蛋白", "磁珠体积(ul)", "提取浓度(ng/ul)",
                "洗脱体积(ul)", "实验异常备注"]

    def get_or_init_instance(self, instance_loader, row):
        instance = self.get_instance(instance_loader, row)
        if instance:
            # instance.operator = BmsUser.objects.get(username=row['操作人员'])
            instance.test_number = row['试剂批号']
            instance.ext_method = row['提取方法']
            instance.objective = row['目的']
            instance.start_number = row['起始取样量(ml)']
            instance.hemoglobin = row['血红蛋白']
            instance.cizhutiji = row['磁珠体积(ul)']
            instance.ext_density = row['提取浓度(ng/ul)']
            instance.elution_volume = row["洗脱体积(ul)"]
            # instance.ext_date = row["提取日期"]
            instance.note = row["实验异常备注"]
            instance.save()
            return instance, False
        else:
            return self.init_instance(row), True

    def init_instance(self, row=None):
        if not row:
            row = {}
        instance = ExtExecute()
        for attr, value in row.items():
            setattr(instance, attr, value)
        if ExtExecute.objects.all().count() == 0:
            instance.id = "1"
        else:
            instance.id = str(int(ExtExecute.objects.latest('id').id) + 1)
        instance.ext_number = row['实验编号']
        # instance.operator = BmsUser.objects.get(username=row['操作人员'])
        instance.test_number = row['试剂批号']
        instance.ext_method = row['提取方法']
        instance.objective = row['目的']
        instance.start_number = row['起始取样量(ml)']
        instance.hemoglobin = row['血红蛋白']
        instance.cizhutiji = row['磁珠体积(ul)']
        instance.ext_density = row['提取浓度(ng/ul)']
        instance.elution_volume = row["洗脱体积(ul)"]
        # instance.ext_date = row["提取日期"]
        instance.note = row["实验异常备注"]
        instance.save()
        return instance


class QualityTestResource(resources.ModelResource):
    class Meta:
        model = QualityTest
        skip_unchanged = True
        import_id_fields = ('qua_number', )
        fields = ('qua_number', "operator", 'test_number', 'template_number',
                  'instrument', "loop_number", 'background_baseline', "noise",
                  'ct', 'amplification_curve', 'is_quality', 'qua_date',
                  "note")
        export_order = (
            'qua_number', "operator", 'test_number', 'template_number',
            'instrument', "loop_number", 'background_baseline', "noise",
            'ct', 'amplification_curve', 'is_quality', 'qua_date',
            "note")

    def get_export_headers(self):
        return ["qua_number", "实验人员", "试剂批号", "上样模板量", "仪器", "循环数",
                "Background/Baseline", "非甲基化内参ACTB_Noise Band",
                "非甲基化内参ACTB_CT值", "非甲基化内参ACTB_扩增曲线",
                "有无质控", "质检日期", "实验异常备注"]

    def get_or_init_instance(self, instance_loader, row):
        instance = self.get_instance(instance_loader, row)
        if instance:
            instance.test_number = row['试剂批号']
            instance.template_number = row['上样模板量']
            # instance.operator = BmsUser.objects.get(username=row['操作人员'])
            instance.instrument = row['仪器']
            instance.loop_number = row['循环数']
            instance.background_baseline = row['Background/Baseline']
            instance.noise = row['非甲基化内参ACTB_Noise Band']
            instance.ct = row['非甲基化内参ACTB_CT值']
            instance.amplification_curve = row["非甲基化内参ACTB_扩增曲线"]
            instance.is_quality = row["有无质控"]
            # instance.qua_date = row["提取日期"]
            instance.note = row["实验异常备注"]
            instance.save()
            return instance, False
        else:
            return self.init_instance(row), True

    def init_instance(self, row=None):
        if not row:
            row = {}
        instance = QualityTest()
        for attr, value in row.items():
            setattr(instance, attr, value)
        if QualityTest.objects.all().count() == 0:
            instance.id = "1"
        else:
            instance.id = str(int(QualityTest.objects.latest('id').id) + 1)
        instance.qua_number = row['实验编号']
        instance.test_number = row['试剂批号']
        # instance.operator = BmsUser.objects.get(username=row['操作人员'])
        instance.template_number = row['上样模板量']
        instance.instrument = row['仪器']
        instance.loop_number = row['循环数']
        instance.background_baseline = row['Background/Baseline']
        instance.noise = row['非甲基化内参ACTB_Noise Band']
        instance.ct = row['非甲基化内参ACTB_CT值']
        instance.amplification_curve = row["非甲基化内参ACTB_扩增曲线"]
        instance.is_quality = row["提取日期"]
        instance.qua_date = row["质检日期"]
        instance.note = row["实验异常备注"]
        instance.save()
        return instance


class BsTaskResource(resources.ModelResource):
    class Meta:
        model = BsTask
        skip_unchanged = True
        import_id_fields = ('bs_number',)
        fields = ('bs_number', "operator", 'test_number', 'bis_begin',
                  'bis_template', "bis_elution", 'is_quality', "operator",
                  'bs_date', 'note')
        export_order = (
            'bs_number', "operator", 'test_number', 'bis_begin',
            'bis_template', "bis_elution", 'is_quality', "operator",
            'bs_date', 'note')

    def get_export_headers(self):
        return ["bs_number", "操作人员", "试剂批号", "BIS起始量(ng)", "BIS模板量(ul)",
                "BIS洗脱体积(ul)",
                "有无质控", "操作人员",
                "BS实验日期", "实验异常备注"]

    def get_or_init_instance(self, instance_loader, row):
        instance = self.get_instance(instance_loader, row)
        if instance:
            instance.test_number = row['试剂批号']
            instance.bis_begin = row['BIS起始量(ng)']
            instance.bis_template = row['BIS模板量(ul)']
            instance.bis_elution = row['BIS洗脱体积(ul)']
            instance.is_quality = row['有无质控']
            # instance.operator = BmsUser.objects.get(username=row['操作人员'])
            # instance.bs_date = row['BS实验日期']
            instance.note = row["实验异常备注"]
            instance.save()
            return instance, False
        else:
            return self.init_instance(row), True

    def init_instance(self, row=None):
        if not row:
            row = {}
        instance = QualityTest()
        for attr, value in row.items():
            setattr(instance, attr, value)
        if BsTask.objects.all().count() == 0:
            instance.id = "1"
        else:
            instance.id = str(int(BsTask.objects.latest('id').id) + 1)
        instance.bs_number = row['实验编号']
        instance.test_number = row['试剂批号']
        instance.bis_begin = row['BIS起始量(ng)']
        instance.bis_template = row['BIS模板量(ul)']
        instance.bis_elution = row['BIS洗脱体积(ul)']
        instance.is_quality = row['有无质控']
        # instance.operator = BmsUser.objects.get(username=row['操作人员'])
        # instance.bs_date = row['BS实验日期']
        instance.note = row["实验异常备注"]
        instance.save()
        return instance


class FluorescenceQuantificationResource(resources.ModelResource):
    class Meta:
        model = FluorescenceQuantification
        skip_unchanged = True
        import_id_fields = ('fq_number', )
        fields = ('fq_number', 'test_number', 'instrument', 'loop_number',
                  "background", 'actb_noise', "actb_ct", "actb_amp",
                  "sfrp2_noise", "sfrp2_ct", "sfrp2_amp", 'sdc2_noise',
                  'sdc2_ct', "sdc2_amp", "is_quality", "operator", "fq_date",
                  "note")
        export_order = (
            'fq_number', 'test_number', 'instrument', 'loop_number',
            "background", 'actb_noise', "actb_ct", "actb_amp",
            "sfrp2_noise", "sfrp2_ct", "sfrp2_amp", 'sdc2_noise',
            'sdc2_ct', "sdc2_amp", "is_quality", "operator", "fq_date",
            "note")

    def get_export_headers(self):
        return ["fq_number", "试剂批号", "仪器", "循环数", "background",
                'actb_noise', "actb_ct", "actb_amp",
                "sfrp2_noise", "sfrp2_ct", "sfrp2_amp", 'sdc2_noise',
                'sdc2_ct', "sdc2_amp",
                "有无质控", "操作人员",
                "荧光定量日期", "实验异常备注"]

    def get_or_init_instance(self, instance_loader, row):
        instance = self.get_instance(instance_loader, row)
        if instance:
            instance.test_number = row['试剂批号']
            instance.instrument = row['仪器']
            instance.loop_number = row['循环数']
            instance.background = row['background']
            instance.actb_noise = row['actb_noise']
            instance.actb_ct = row['actb_ct']
            instance.actb_amp = row['actb_amp']
            instance.sfrp2_noise = row['sfrp2_noise']
            instance.sfrp2_ct = row['sfrp2_ct']
            instance.sfrp2_amp = row['sfrp2_amp']
            instance.sdc2_noise = row['sdc2_noise']
            instance.sdc2_ct = row['sdc2_ct']
            instance.sdc2_amp = row['sdc2_amp']
            instance.is_quality = row['有无质控']
            instance.note = row['实验异常备注']

            # instance.operator = BmsUser.objects.get(username=row['操作人员'])
            # instance.bs_date = row['BS实验日期']
            instance.note = row["实验异常备注"]
            instance.save()
            return instance, False
        else:
            return self.init_instance(row), True

    def init_instance(self, row=None):
        if not row:
            row = {}
        instance = QualityTest()
        for attr, value in row.items():
            setattr(instance, attr, value)
        if FluorescenceQuantification.objects.all().count() == 0:
            instance.id = "1"
        else:
            instance.id = str(
                int(FluorescenceQuantification.objects.latest('id').id) + 1)
        instance.fq_number = row['实验编号']
        instance.test_number = row['试剂批号']
        instance.bis_begin = row['BIS起始量(ng)']
        instance.bis_template = row['BIS模板量(ul)']
        instance.bis_elution = row['BIS洗脱体积(ul)']
        instance.is_quality = row['有无质控']
        # instance.operator = BmsUser.objects.get(username=row['操作人员'])
        instance.bs_date = row['BS实验日期']
        instance.note = row["实验异常备注"]
        instance.save()
        return instance
