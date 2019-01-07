from django.test import TestCase
from projects.models import ContractsInfo


class TestProject(TestCase):

    def setUp(self):
        print('开始测试合同模型')

    def tearDown(self):
        print('结束测试')

    def test_can_create_contract(self):
        test_contract = ContractsInfo.objects.create(
            contract_id="XXXXX", contract_number="xxxxxxxx"
        )
        self.assertTrue(test_contract)
