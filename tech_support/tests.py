from django.test import TestCase
from tech_support.models import *
from accounts.models import BmsUser

class Exptest(TestCase):

    def setUp(self):
        print("********setUp*******")
        user = BmsUser.objects.create(
            username="TECH", password="TEST_123456"
        )
        self.assertTrue(user)

    def test_task(self):
        print("********test_task*******")
        boxd = BoxDeliveries.objects.create(ext_number="T0000000002")
        box = Boxes.objects.create(qua_number="Q0000000001")
        extm = ExtMethod.objects.create(bs_number="B000000001")
        ext = ExtSubmit.objects.create(fq_number="F0000000001")
        self.assertTrue(boxd)
        self.assertTrue(box)
        self.assertTrue(extm)
        self.assertTrue(ext)

    def test_get_object_test(self):
        print("********test_get_object_test**************")
        boxd = BoxDeliveries.objects.get(ext_number="T0000000002")
        box = Boxes.objects.get(qua_number="Q0000000001")
        extm = ExtMethod.objects.get(bs_number="B000000001")
        ext = ExtSubmit.objects.get(fq_number="F0000000001")
        print(boxd, "***", box, "***", extm,"***",ext)


