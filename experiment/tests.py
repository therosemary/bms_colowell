from django.test import TestCase
from experiment.models import *
from accounts.models import BmsUser


class Exptest(TestCase):

    def setUp(self):
        print("********setUp*******")
        ext = ExtExecute.objects.create(ext_number="T0000000001")
        self.assertTrue(ext)
        user = BmsUser.objects.create(
            username="TDD_TEST_USER", password="TDD_TEST_USER_123456"
        )
        self.assertTrue(user)

    def test_task(self):
        print("********test_task*******")
        ext1 = ExtExecute.objects.create(ext_number="T0000000002")
        qua = QualityTest.objects.create(qua_number="Q0000000001")
        bs = BsTask.objects.create(bs_number="B000000001")
        fq = FluorescenceQuantification.objects.create(fq_number="F0000000001")
        self.assertTrue(ext1)
        self.assertTrue(qua)
        self.assertTrue(bs)
        self.assertTrue(fq)
        ext = ExtExecute.objects.get(ext_number="T0000000002")
        ext1 = ExtExecute.objects.get(ext_number="T0000000001")
        print(ext,ext1)
        qua = QualityTest.objects.get(qua_number="Q0000000001")
        bs = BsTask.objects.get(bs_number="B000000001")
        fq = FluorescenceQuantification.objects.get(fq_number="F0000000001")
        print(qua, "***", bs, "***", fq)

    def test_get_object_test(self):
        print("********test_get_object_test**************")
        ext = ExtExecute.objects.get(ext_number="T0000000002")
        print(ext)
        qua = QualityTest.objects.get(qua_number="Q0000000001")
        bs = BsTask.objects.get(bs_number="B000000001")
        fq = FluorescenceQuantification.objects.get(fq_number="F0000000001")
        print(qua, "***", bs, "***", fq)


    def test_login(self):
        print("**********TEST_LOGIN************")
        resp_login = self.client.post("/admin/login/", data={
            "username":"TDD_TEST_USER", "password":"TDD_TEST_USER_123456"
        })
        print(resp_login.__dict__)