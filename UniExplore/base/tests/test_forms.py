from django.test import SimpleTestCase
from ..forms import *
from datetime import date


class TestForms(SimpleTestCase):
    
    def test_login_form_valid_data(self):
        form = UserRegisterForm(data = {
            'username':"test123",
            'first_name': "test",
            'last_name': "tset",
            'email':"test@exeter.ac.uk",
            'password1': "password",
            'password2': "password"
        })

        self.assertTrue(form.is_valid)
    
    def test_challenge_form_valid_data(self):
        form = ChallengeForm(data = {
            'category':"photography",
            'name': "challenge 1",
            'points': "100",
            'description':"this is a description",
            'long': "23.23",
            "lat": "32.22",
            'expires_on': str(date.today())
        })
        self.assertTrue(form.is_valid)
    
    def test_response_form_valid_data(self):
        form = ResponseForm(data = {
            'description':"this is a fake description",
            'photograph': "test/img/dog.png",
        })
        self.assertTrue(form.is_valid)

    def test_response_form_valid_data(self):
        form = commentForm(data = {
            'text': "this is a comment"
        })
        self.assertTrue(form.is_valid)
    
    def test_response_form_valid_data(self):
        form = UserUpdateForm(data = {
            'username':"newUsername"
        })
        self.assertTrue(form.is_valid)

    def test_response_form_valid_data(self):
        form = ProfileUpdateForm(data = {
            'bio': "this is a fake bio",
            'university': "Exeter university",
            'picture': "test/img/dog.png",
        })
        self.assertTrue(form.is_valid)



    def test_challenge_form_no_data(self):
        form = ChallengeForm(data = {})
        self.assertEquals(len(form.errors), 7)

    def test_response_form_no_data(self):
        form = ResponseForm(data = {})
        self.assertEquals(len(form.errors), 1)

    def test_profile_form_no_data(self):
        form = ProfileForm(data = {})
        self.assertEquals(len(form.errors), 8)

    def test_comment_form_no_data(self):
        form = commentForm(data = {})
        self.assertEquals(len(form.errors), 1)

    def test_user_update_form_no_data(self):
        form = UserUpdateForm(data = {})
        self.assertEquals(len(form.errors), 1)
    
    def test_profile_update_form_no_data(self):
        form = ProfileUpdateForm(data = {})
        self.assertEquals(len(form.errors), 2)

    def test_login_form_no_data(self):
        form = UserRegisterForm(data = {})
        self.assertEquals(len(form.errors), 6)