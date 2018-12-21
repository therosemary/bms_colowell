from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone
from accounts.models import BmsUser
from partners.models import *


class TestPartners(TestCase):
    
    def setUp(self):
        self.test_user = BmsUser.objects.create_user(
            username="TDD_TEST_USER", password="TDD_TEST_USER_fef123",
            is_superuser=True, is_staff=True, is_active=True,
        )
        self.login_data = {
            'username': "TDD_TEST_USER",
            'password': "TDD_TEST_USER_fef123",
        }
    
    def tearDown(self):
        self.test_user.delete()
    
    def test_can_login_admin(self):
        result = self.client.login(**self.login_data)
        self.assertTrue(result)

    def test_can_create_partner(self):
        test_partner = Partners.objects.create(
            code="TDD_TEST_PARTNER_0001", bms_user=self.test_user
        )
        self.assertTrue(test_partner)
    
    def test_can_create_propaganda_no_bms_user(self):
        test_partner = Partners.objects.create(
            code="TDD_TEST_PARTNER_0001", bms_user=self.test_user
        )
        with self.assertRaises(IntegrityError):
            Propaganda.objects.create(partner=test_partner)

    def test_can_create_propaganda(self):
        test_partner = Partners.objects.create(
            code="TDD_TEST_PARTNER_0001", bms_user=self.test_user
        )
        propaganda = Propaganda.objects.create(
            partner=test_partner, date=timezone.now(), bms_user=self.test_user
        )
        self.assertTrue(propaganda)
