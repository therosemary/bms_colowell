from django.test import TestCase
from accounts.models import *


class TestAccounts(TestCase):
    
    def setUp(self):
        self.user = BmsUser.objects.create_user(
            username="TDD_TEST_USER", password="TDD_TEST_USER_123456"
        )
    
    def tearDown(self):
        self.user.delete()
    
    def test_can_create_dingtalk_info(self):
        dingtalk_info = DingtalkInfo.objects.create(
            userid="fewfd1223123", bms_user=self.user
        )
        self.assertTrue(dingtalk_info)
    
    def test_can_create_wechat_info(self):
        wechat_info = WechatInfo.objects.create(
            openid="fewfd1223123", bms_user=self.user
        )
        self.assertTrue(wechat_info)
