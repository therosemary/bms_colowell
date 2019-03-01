from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, DateWidget
from tech_support.models import Boxes, BoxDeliveries
import datetime

Monthchoose = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G",
               8: "H", 9: "I", 10: "G", 11: "K", 12: "L", }


class BoxesResource(resources.ModelResource):
    id = Field(
        column_name='盒子编号', attribute='id', default=None
    )
    deliver_number = Field(
        column_name="盒子发货编号", attribute="box_deliver__index_number")
    bar_code = Field(
        column_name="盒子条形码", attribute="bar_code"
    )

    class Meta:
        model = Boxes
        skip_unchanged = True
        # import_id_fields = ('bar_code',)
        fields = ('id', 'deliver_number', 'bar_code')
        export_order = ('id', 'deliver_number', 'bar_code')

    def export(self, queryset=None, *args, **kwargs):
        queryset_result = Boxes.objects.filter(id=None)
        for i in queryset:
            queryset_result |= Boxes.objects.filter(box_deliver=i)
        return super().export(queryset=queryset_result, *args, **kwargs)

    def get_export_headers(self):
        return ["盒子编号", "盒子发货编号", "盒子条形码"]

    def dehydrate_deliver_number(self, boxes):
        return boxes.box_deliver.index_number

    def init_instance(self, row=None):
        sj = datetime.datetime.now()
        if not row:
            row = {}
        instance = Boxes()
        for attr, value in row.items():
            setattr(instance, attr, value)
        if Boxes.objects.all().count() == 0:
            instance.id = "1"
            instance.index_number = "HZ" + str(sj.year) + \
                                    Monthchoose[
                                        sj.month] + "1"
        else:
            instance.id = str(int(Boxes.objects.latest('id').id) + 1)
            instance.index_number = "HZ" + str(sj.year) + \
                                    Monthchoose[
                                        sj.month] + str(
                Boxes.objects.latest('id').id + 1)
        instance.box_deliver = BoxDeliveries.objects.get(
            index_number=row["盒子发货编号"])

        instance.bar_code = row["盒子条形码"]
        return instance
