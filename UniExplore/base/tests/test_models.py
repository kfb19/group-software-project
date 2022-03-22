from django.test import TestCase
from ..models import *
from model_bakery import baker
class TestModels(TestCase):
    
        

    def test_model_creations(self):
        try:
            user = baker.make(User, _quantity=10)

            catagoties = baker.make(Category, _quantity=5)
            
            challenges = baker.make(Challenges, _quantity=10)
             
            responses = baker.make(Responses, _quantity=20, liked=baker.make(User, _quantity=2), challenge=baker.make(Challenges))

            dailyRiddleResponses = baker.make(DailyRiddle, _quantity=3)

            comments = baker.make(Comments, _quantity=100, user=baker.make(User), response=responses[0])
            
            likes = baker.make(Likes, _quantity=100, user=baker.make(User), response=responses[0])

            upgrade = baker.make(Upgrade, user=baker.make(User))

            assert True
        except Exception:
            assert False

    def test_response_save_model(self):
        response = baker.make(Responses, liked=baker.make(User, _quantity=2), challenge=baker.make(Challenges))
        try:
            response.save()
            assert True
        except Exception:
            assert False
    
    def test_profile_save_model(self):
        profile = baker.make(Profile, user=baker.make(User))
        try:
            profile.save()
            assert True
        except Exception:
            assert False
