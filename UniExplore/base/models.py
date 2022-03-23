"""
Authors: 
    - Michael Hills
    - Kate Belson 
    - Tomas Premoli
    - Lucas Smith
"""

from django.contrib.auth.models import User
from axes.models import AccessAttempt
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from PIL import Image
from io import BytesIO
import os
import sys


# File name setting for profile pics (Tomas Premoli)
def pfp_location(instance, filename):
    type = filename.split('.')[-1]
    filename = str(hash(instance.user.id)) + "." + type
    return os.path.join('profile_pictures/', filename)


# Model for a user profile (Michael Hills, Lucas Smith, Tomas Premoli)
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    points = models.IntegerField(default=0, null=True)
    bio = models.CharField(default="No bio set.", max_length=200)
    university = models.CharField(default="No university set.", max_length=200)  # TODO: Dropdown for available unis?
    picture = models.ImageField(default='profile_pictures/placeholder.png', upload_to=pfp_location)
    email_confirmed = models.BooleanField(default=False)
    following = models.ManyToManyField('Profile', related_name="following_profile", blank=True)

    def __str__(self) -> str:
        return self.name

    # overrides image data to be compressed (Tomas Premoli)
    def save(self, *args, **kwargs):
        try:
            # Opening the uploaded image
            img = Image.open(self.picture)
            output = BytesIO()
            # Resize/modify the image
            width, height = img.size

            offset  = int(abs(height-width)/2)

            # This crops the image into a square depending if portrait or landscape
            if width==height:
                pass
            elif width>height:
                img = img.crop([offset,0,width-offset,height])
            else:
                img = img.crop([0,offset,width,height-offset])

            
            img = img.resize(settings.PROFILE_PIC_SIZE)


            img = img.convert('RGB')
            # after modifications, save it to the output
            img.save(output, format='JPEG', quality=settings.PROFILE_PIC_QUALITY)
            output.seek(0)

            # Set field to modified picture
            self.picture = InMemoryUploadedFile(output, 'ImageField', 
                                            "%s.jpg" % str(hash(self.picture.name.split('.')[0])), 
                                            'image/jpeg', sys.getsizeof(output), None)
        except: pass
        super(Profile, self).save()


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


# Model the daily riddle (Michael Hills)
class DailyRiddle(models.Model):
    name = models.CharField(max_length=200, null=True)
    points = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    lat = models.FloatField(default=0)
    long = models.FloatField(default=0)
    answer = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


# Model for completed daily riddles (Michael Hills)
class CompleteRiddle(models.Model):
    riddle = models.ForeignKey(DailyRiddle, related_name='complete_riddle', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# File name setting for profile pics (Tomas Premoli)
def response_pic_location(instance, filename):
    type = filename.split('.')[-1]
    filename = str(hash(str(instance.user.id) + "-" + str(instance.challenge.id))) + "." + type

    return os.path.join('image_uploads/', filename)

# Model for the responses to challenges (Michael Hills, Tomas Premoli)
class Responses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    photograph = models.ImageField(upload_to=response_pic_location, default='image_uploads/challenge-completed.png')
    challenge = models.ForeignKey(Challenges, related_name='challenge_response', on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')

    def __str__(self):
        return str(self.id)

    # overrides image data to be compressed (Tomas Premoli)
    def save(self, *args, **kwargs):
        maxwidth = settings.RESPONSE_PHOTO_SIZE[0]
        maxheight = settings.RESPONSE_PHOTO_SIZE[1]

        # Opening the uploaded image
        img = Image.open(self.photograph)
        output = BytesIO()
        # Resize/modify the image
        width, height = img.size

        # This resizes image retaining aspect ratio
        if width>height:
            width_percent = (maxwidth/float(img.size[0]))
            h_size = int((float(height)*float(width_percent)))

            img = img.resize((maxwidth,h_size))
            img = img.convert('RGB')
        else:
            height_percent = (maxheight/float(img.size[1]))
            w_size = int((float(width)*float(height_percent)))

            img = img.resize((w_size,maxheight))
            img = img.convert('RGB')

            
        # after modifications, save it to the output
        img.save(output, format='JPEG', quality=settings.RESPONSE_PHOTO_QUALITY)
        output.seek(0)

        # Set field to modified picture
        self.photograph = InMemoryUploadedFile(output, 'ImageField',
                                               "%s.jpg" % str(hash(self.photograph.name.split('.')[0])),
                                               'image/jpeg', sys.getsizeof(output), None)

        super(Responses, self).save()

    # Number of likes of a challenge
    @property
    def num_likes(self):
        return self.liked.all().count()

    # The options for the like button (Michael Hills)


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


# Model for comments on a response (Michael Hills)
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.ForeignKey(Responses, related_name="comments", on_delete=models.CASCADE)
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


# Model for requests to become a gamemaster (Michael Hills)
class Upgrade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
# Model for reported posts (Kate Belson)
class ReportPosts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

# Model for reported posts (Kate Belson)
class ReportComments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


