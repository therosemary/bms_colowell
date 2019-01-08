from django.test import TestCase
from intentions.models import Intentions
from accounts.models import BmsUser


class TestIntention(TestCase):
    """意向池信息（Intentions)测试类"""

    def setUp(self):
        self.test_user = BmsUser.objects.create_user(
            username="TDD_TEST_USER", password="TDD_TEST_USER_fef123",
            is_superuser=True, is_staff=True, is_active=True,
        )

    def tearDown(self):
        self.test_user.delete()

    def test_can_create_intention(self):
        """测试用例：新建客户意向信息"""
        test_intention = Intentions.objects.create(
            intention_client="某代理商", contact_number="12345676",
            items="代理医学产品销售", fill_name=self.test_user
        )
        self.assertTrue(test_intention)
