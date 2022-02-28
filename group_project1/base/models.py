from django.contrib.auth.models import User

from axes.models import AccessAttempt
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    points = models.IntegerField(default=0, null=True)
    bio = models.CharField(default="No bio set.", max_length=200)
    university = models.CharField(default="Uni of Exeter", max_length=200) #TODO: Dropdown for available unis?
    # TODO: Implement profile pics

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
    lat = models.FloatField(default=0)
    long = models.FloatField(default=0)

    def __str__(self):
        return str(self.name)


class Responses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    challenge = models.ForeignKey(Challenges, related_name='challenge_response', on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class AccessAttemptAddons(models.Model):
    accessattempt = models.OneToOneField(AccessAttempt, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField(_("Expiration Time"), auto_now_add=False)
