from django.db import models
from django.core.files.base import File
from django.db.models import CharField, Model

class User(models.Model):
    authorName = models.CharField(max_length=15, default="user", blank=False, null=False)
    rollNumber = models.CharField(max_length=10)

    def __str__(self):
        return self.authorName


class VideoContent(models.Model):
    file = models.URLField(blank=False, null=False)
    subject = models.CharField(max_length=101)
    year = models.IntegerField(default=0)
    semester = models.IntegerField(default=0)
    uploadedBy = models.CharField(max_length=20, blank=True, null=True)
    speaker = models.CharField(max_length=100, blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.file.name

class Comments(models.Model):
    #author = models.OneToOneField(User, default="author", on_delete = models.CASCADE)
    author = models.CharField(max_length=100)
    commentBody = models.CharField(default="", max_length=1000)
    videocontent = models.ForeignKey(VideoContent, default=None, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.author
