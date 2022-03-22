from django.test import TestCase
from ..models import *

class TestModels(TestCase):
    
    def setUP(self):
        self.user = User.objects.create(
            username="test"
            

        )