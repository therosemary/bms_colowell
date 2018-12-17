from selenium import webdriver


# To test the installation of Django
broswer = webdriver.Chrome()
broswer.get("http://127.0.0.1:8000")
assert "Django" in broswer.title