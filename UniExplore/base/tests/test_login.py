"""
Authors: 
    - Conor Behard Roberts
"""

from time import time
from django.test import TestCase
from datetime import datetime, timezone
from ..models import CompleteRiddle, DailyRiddle, Profile, User, Category, Challenges, Responses


class ModelTesting(TestCase):

    def setUp(self):
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

    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)
        self.assertNotEqual(user_count, 0)
    
    def test_user_password(self):
        self.assertTrue(self.user.check_password(self.password))

    def test_login_url(self):
        login_url = "/login/"
        data = {"username": self.username, "password": self.password}
        response = self.client.post(login_url, data, follow=True)
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        


        # self.profile = Profile.objects.create(user=self.user, name="test_name")

        # self.category = Category.objects.create(name="test_name")

        # self.challenge = Challenges.objects.create(user=self.user,
        #                                            category=self.category,
        #                                            name="test_name",
        #                                            points=0,
        #                                            description="test_description",
        #                                            created=datetime.now(),
        #                                            lat=0.25,
        #                                            long=20.23)

        # # self.response = Responses.objects.create(user=self.user,
        # #                                          description="test_description",
        # #                                          challenge=self.challenge,
        # #                                          created=datetime.now(),
        # #                                          )

        # self.response = DailyRiddle.objects.create(name='test',
        #                                             points = 0,
        #                                             created=datetime.now(),
        #                                             lat = 0.23,
        #                                             long=20,
        #                                             answer='test answer')
