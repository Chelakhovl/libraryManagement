import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test import TestCase
from decouple import config



class LoginSeleniumTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        service = Service('C:\\Users\\Пользователь\\Desktop\\chromedriver\\chromedriver.exe')
        cls.driver = webdriver.Chrome(service=service)
        cls.driver.maximize_window()
        cls.driver.get('http://127.0.0.1:8000/')

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_valid_login(self):
        log_in = self.driver.find_element(By.XPATH, '/html/body/header/nav/div/form/button')
        log_in.click()
        time.sleep(5)

        email_input = self.driver.find_element(By.NAME, 'username')
        email_input.clear()
        email_input.send_keys(config('EMAIL'))

        password_input = self.driver.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys(config('PASSWORD'))

        password_input.send_keys(Keys.RETURN)
        time.sleep(5)

        if 'My account' in self.driver.page_source:
            print("Login successful!")
        else:
            print("Login failed!")

        my_account_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'btn-outline-success'))
        )
        my_account_button.click()

        log_out_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/main/form[1]/button'))
        )
        log_out_button.click()

    def test_invalid_login(self):
        log_in = self.driver.find_element(By.XPATH, '/html/body/header/nav/div/form/button')
        log_in.click()
        time.sleep(5)

        email_input = self.driver.find_element(By.NAME, 'username')
        email_input.clear()
        email_input.send_keys('leo@gmail.com')

        password_input = self.driver.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys('wrong_password')

        password_input.send_keys(Keys.RETURN)
        time.sleep(5)

        if 'Log out' not in self.driver.page_source:
            print("Login failed as expected!")
        else:
            print("Login should not have been successful!")
