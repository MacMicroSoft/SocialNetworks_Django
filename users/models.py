from django.contrib.auth.models import User
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField

# Create your models here.
User._meta.get_field('email')._unique = True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = ThumbnailerImageField(
        upload_to='profile_images',
        resize_source=dict(
            quality=95,
            size=(300, 300),
            sharpen=True
        ),
        default='profile.png'
    )
    bio = models.TextField(max_length=255)

    def get_absolute_url(self):
        return self.avatar.url

    def __str__(self):
        return self.user.username

