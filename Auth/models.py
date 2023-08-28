from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user=models.IntegerField(default=0)
    leetcode_link=models.URLField(max_length=200)
    codechef_link=models.URLField(max_length=200)
    github_link=models.URLField(max_length=200)

class Notes(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    video_id=models.CharField(max_length=1000)
    content=models.TextField(max_length=1000)


