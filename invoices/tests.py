import datetime
from django.test import TestCase
from projects.models import ContractsInfo, InvoiceInfo
from accounts.models import BmsUser
from .models import SendInvoices


class TestInvoices(TestCase):
    """寄送发票（SendInvoices）测试类"""

    def setUp(self):
        self.test_user = BmsUser.objects.create(
            username="TDD_TEST_USER", password="TDD_TEST_USER_123456"
        )
        self.test_username = "TDD_TEST_USER"
        self.test_contract = ContractsInfo.objects.create(
            contract_id="YX201907010000001234", contract_number="xxxxxxxx",
            staff_name=self.test_user,
        )
        self.test_invoice = InvoiceInfo.objects.create(
            invoice_id="YX201901071441251234", contract_id=self.test_contract,
            apply_name=self.test_username
        )

    def tearDown(self):
        # TODO:20190108 删除self.test_user字段，测试不通过
        self.test_contract.delete()
        self.test_invoice.delete()

    def test_can_create_invoice(self):
        """测试用例：在数据库新建寄送发票的信息"""
        test_send_invoice = SendInvoices.objects.create(
            invoice_id=self.test_invoice, billing_date=datetime.datetime.now(),
            fill_name=self.test_username
        )
        self.assertTrue(test_send_invoice)
