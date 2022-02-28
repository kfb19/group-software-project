from django.test import TestCase
from datetime import datetime
from .models import Profile, User, Category, Challenges, Responses


class ModelTesting(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test_username",
                                             first_name="test_first_name",
                                             last_name="test_last_name",
                                             email="test@email.com")

        self.profile = Profile.objects.create(user=self.user, name="test_name")

        self.category = Category.objects.create(name="test_name")

        self.challenge = Challenges.objects.create(user=self.user,
                                                   category=self.category,
                                                   name="test_name",
                                                   points=0,
                                                   description="test_description",
                                                   created=datetime.now(),
                                                   lat=0.25,
                                                   long=20.23)

        self.response = Responses.objects.create(user=self.user,
                                                 description="test_description",
                                                 challenge=self.challenge,
                                                 created=datetime.now())

    def test_profile_model(self):
        data = self.profile
        self.assertTrue(isinstance(data, Profile))
        self.assertEqual(str(data), "test_name")

    def test_category_model(self):
        data = self.category
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), "test_name")

    def test_challanges_model(self):
        data = self.challenge
        self.assertTrue(isinstance(data, Challenges))
        self.assertEqual(str(data), "test_name")

    def test_response_model(self):
        data = self.response
        self.assertTrue(isinstance(data, Responses))
        self.assertEqual(str(data), '1')
