from django.test import TestCase
from accounts.models import *


class TestAccounts(TestCase):
    
    def setUp(self):
        print("【用户管理】test start\n")
    
    def tearDown(self):
        print("【用户管理】test done\n")

    def test_can_create_bms_user(self):
        user = BmsUser.objects.create_user(
            username="TDD_TEST_USER", password="TDD_TEST_USER_123456"
        )
        self.assertTrue(user)
        
    def test_can_create_dingtalk_info(self):
        user = BmsUser.objects.get(username="TDD_TEST_USER")
        dingtalk_info = DingtalkInfo.objects.create(
            userid="fewfd1223123", bms_user=user
        )
        self.assertTrue(dingtalk_info)
    