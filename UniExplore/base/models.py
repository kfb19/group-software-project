"""
Authors: 
    - Michael Hills
    - Kate Belson (some edits) 
    - Tomas Premoli
"""

from django.contrib.auth.models import User
from axes.models import AccessAttempt
from django.db import models
from django.utils.translation import gettext_lazy as _
import os


# File name setting for profile pics (Tomas Premoli)
def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = str(instance.user.id) + "." + ext
    existing = [filename for filename in os.listdir('media/profile_pictures/') if filename.startswith(str(instance.user.id) + ".")]
    if len(existing) > 0:
        os.remove(os.path.join('media/profile_pictures/', existing[0]))
    return os.path.join('profile_pictures/', filename)

# Model for a user profile (Michael Hills, Lucas Smith)
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    points = models.IntegerField(default=0, null=True)
    bio = models.CharField(default="No bio set.", max_length=200)
    university = models.CharField(default="No university set.", max_length=200)  # TODO: Dropdown for available unis?
    picture = models.ImageField(default='profile_pictures/placeholder.png', upload_to=content_file_name)

    def __str__(self) -> str:
        return self.name

# Model for a category of challenges (Michael Hills)

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

# Model for the challenges (Michael Hills)


class Challenges(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    points = models.IntegerField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    expires_on = models.DateTimeField(default="2025-01-01")
    is_weekly_challenge = models.BooleanField(default=False)
    lat = models.FloatField(default=0)
    long = models.FloatField(default=0)

    def __str__(self):
        return str(self.name)

# Model for the responses to challenges (Michael Hills)


class Responses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    photograph = models.ImageField(upload_to='image_uploads', default = 'image_uploads/challenge-completed.png')
    challenge = models.ForeignKey(Challenges, related_name='challenge_response', on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')

    def __str__(self):
        return str(self.id)

    # Number of likes of a challenge
    @property
    def num_likes(self):
        return self.liked.all().count()

    # The options for the like button (Michael Hills)
LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)



class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.ForeignKey(Responses,related_name="comments", on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

# Model for the likes of a post (Michael Hills)
class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.ForeignKey(Responses, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.response)


class AccessAttemptAddons(models.Model):
    accessattempt = models.OneToOneField(AccessAttempt, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField(_("Expiration Time"), auto_now_add=False)
