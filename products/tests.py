from django.test import TestCase, Client
from accounts.models import BmsUser
from products.models import Products


class TestProducts(TestCase):
    
    def setUp(self):
        self.test_user = BmsUser.objects.create_user(
            username="TDD_TEST_USER", password="TDD_TEST_USER_123456"
        )
        self.login_data = {
            'username': "TDD_TEST_USER",
            'password': "TDD_TEST_USER_fef123",
        }
    
    def tearDown(self):
        self.test_user.delete()
    
    def test_can_create_product(self):
        product = Products.objects.create(
            barcode="CYS000",
        )
        self.assertTrue(product)
    
    def test_can_post_an_product(self):
        # 这里提交的测试数据其实是非法的，但是单元测试测不出来，
        # 需要在实际页面里面提交非法的barcode测试
        resp_login = self.client.post("/admin/login/", data=self.login_data)
        resp_product = self.client.post(
            "/admin/products/products/add/", data={"barcode": "CYS0000"}
        )
        self.assertEqual(resp_login.status_code, 200)
        self.assertEqual(resp_product.status_code, 302)
