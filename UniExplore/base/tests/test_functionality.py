import imp
from turtle import home
from django.forms import SelectDateWidget
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from ..models import CompleteRiddle, DailyRiddle, Profile, User, Category, Challenges, Responses
import time

class TestPages(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('chromedriver.exe')
        self.username = "test"
        self.first_name = "first name"
        self.last_name = "last name"
        self.email = "test@email.com"
        self.password = "password_123"

        self.user = User(username=self.username, first_name=self.first_name, last_name=self.last_name, email=self.email, password=self.password)
        self.user.is_staff = True
        self.user.is_superuser=True
        self.user.set_password(self.password)
        self.user.save()
        

    def tearDown(self):
        self.browser.close()
        pass

    def test_login_page(self):
        self.browser.get(self.live_server_url)
        # The user requests the page for the first time
        try:
            self.browser.find_element_by_class_name('login-form')
            assert True
        except Exception:
            assert False

    def test_register_login(self):
        self.browser.get(self.live_server_url)
        # login
        self.browser.find_element_by_name('username').send_keys(self.username)
        self.browser.find_element_by_name('password').send_keys(self.password)
        self.browser.find_element_by_id('submit').click()
        home_url = self.live_server_url + reverse('home')

        self.assertEqual(home_url, self.browser.current_url)
        