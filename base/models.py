from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)


    def __str__(self) -> str:
        return self.name



class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

class Challenges(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    points = models.IntegerField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str(self.name)
