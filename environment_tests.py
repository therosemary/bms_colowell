import unittest
from selenium import webdriver


class TheFirstTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()
    
    def test_can_start_a_page(self):
        self.browser.get("http://127.0.0.1:8000")
        self.assertIn("Django", self.browser.title)


if __name__ == '__main__':
    unittest.main(warnings="ignore")