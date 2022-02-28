from msilib.schema import ReserveCost
from tkinter import CASCADE
from django.contrib.auth.models import User

from axes.models import AccessAttempt
from django.db import models
from django.utils.translation import gettext_lazy as _

# Model for a user profile
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    points = models.IntegerField(default=0, null=True)

    def __str__(self) -> str:
        return self.name

# Model for a category of challenges
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

# Model for the challenges
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

# Model for the responses to challenges
class Responses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    challenge = models.ForeignKey(Challenges, related_name='challenge_response', on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')

    def __str__(self):
        return str(self.id)

    # Number of likes of a challenge
    @property
    def num_likes(self):
        return self.liked.all().count()

    # The options for the like button
LIKE_CHOICES = (
    ('Like','Like'),
    ('Unlike','Unlike'),
)


# Model for the likes of a post
class Likes(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    response = models.ForeignKey(Responses, on_delete = models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.response)




class AccessAttemptAddons(models.Model):
    accessattempt = models.OneToOneField(AccessAttempt, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField(_("Expiration Time"), auto_now_add=False)
