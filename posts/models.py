from django.db import models
from users.models import Profile, User


class Tags(models.Model):
    tags = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.tags


class Images(models.Model):
    image = models.FileField(upload_to='posts_images')

    def get_absolute_url(self):
        return self.image.url


class Posts(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comments = models.TextField(max_length=255)
    tags = models.ManyToManyField(Tags, unique=False)
    date = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(Profile, related_name='post_like', blank=True)
    images = models.ManyToManyField(Images, blank=False)

    def number_of_likes(self):
        return self.like.count()

