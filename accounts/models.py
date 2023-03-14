from django.db import models
from django.contrib.auth.models import User
from blog.models import user_directory_path
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

# Create your models here.

# customer path to store my image data or store the user's avatar images
def user_directory_path(instance, filename):
    return 'user/avatars/{0}/{1}'.format(instance.user.id, filename)


# one to one connection between this table and the users table
# on_delete means it should delete a user in the user table and also should delete the user in this profile table
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # the user profile img
    avatar = models.ImageField(upload_to=user_directory_path, default='user/avatar.jpg')
    bio = models.TextField(max_length=500, blank=True)

    # to check the size of the image user profile updating
    def clean(self):
        if not self.avatar:
            raise ValidationError("x")
        else:
            w, h = get_image_dimensions(self.avatar)
            if w != 200:
                raise ValidationError("x")
            if h != 200:
                raise ValidationError("x")

    def __str__(self):
        return self.user.username


@ receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)