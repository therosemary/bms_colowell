from django.test import TestCase
from projects.models import ContractsInfo, BoxApplications, InvoiceInfo
from accounts.models import BmsUser
from partners.models import Partners

class TestProject(TestCase):
    """projects模块测试类"""

    def setUp(self):
        self.test_user = BmsUser.objects.create_user(
            username="TDD_TEST_USER", password="TDD_TEST_USER_123456"
        )
        self.test_partner = Partners.objects.create(
            code="TDD_TEST_PARTNER_0001", bms_user=self.test_user
        )
        self.test_username = "TDD_TEST_USER"

    def tearDown(self):
        self.test_partner.delete()

    def test_can_create_contract(self):
        """测试用例：新建合同信息"""
        self.test_contract = ContractsInfo.objects.create(
            contract_id="YX201907010000001234", contract_number="xxxxxxxx",
            staff_name=self.test_user,
        )
        self.assertTrue(self.test_contract)

    def test_can_create_box(self):
        """测试用例：新建申请盒子记录"""
        test_box = BoxApplications.objects.create(
            amount=30, use="零售", proposer=self.test_username
        )
        self.assertTrue(test_box)

    def test_can_create_invoice(self):
        """测试用例：新建申请发票记录"""
        self.test_contract = ContractsInfo.objects.create(
            contract_id="YX201907010000001234", contract_number="xxxxxxxx",
            staff_name=self.test_user,
        )
        test_invoice = InvoiceInfo.objects.create(
            invoice_id="YX201901071441251234", contract_id=self.test_contract,
            apply_name=self.test_username
        )
        self.assertTrue(test_invoice)
