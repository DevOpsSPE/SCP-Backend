from __future__ import unicode_literals
from django.db import models
from django.core.files.base import File
from django.db.models import CharField, Model
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import FileExtensionValidator

"""
USER MODEL
Wrote a custom model based on the User model of django
We have to write UserManager before User model to overwrite few functionalities as per our requirement
"""

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password and other details
        normalize_email() makes domain name to lowercase for it to be case insensitive
        set_password() is for password encryption
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('role', 'Student')
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=15, default="Student")
    rollNumber = models.CharField(max_length=15, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'rollNumber'
    REQUIRED_FIELDS = ['role','email','username']

"""
END OF USER MODEL
"""

#adding a comment
class File(models.Model):
    file = models.FileField(blank=False, null=False, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    author = models.CharField(max_length=141,default="Admin")
    subject = models.CharField(max_length=101)
    year = models.IntegerField()
    resourceType = models.CharField(max_length=20, blank=True, null=True)
    semester = models.IntegerField()
    numberofUpvotes = models.IntegerField(default=0)
    numberofDownvotes = models.IntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    verified = models.BooleanField(default=False)

class Interview(models.Model):
    name = models.CharField(max_length=141)
    title = models.CharField(max_length=101)
    yearPlaced = models.IntegerField()
    experience = models.CharField(max_length=2000, blank=True, null=True)
    yearPassout = models.IntegerField()
    company = models.CharField(max_length=20,default="")
    numberofUpvotes = models.IntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    verified = models.BooleanField(default=False)

class emailVerify(models.Model):
    rollNumber = models.CharField(max_length=10, primary_key=True)
    email = models.EmailField(max_length=100)
    otp = models.IntegerField()

    def __str__(self):
        return self.otp

class CommentsPYQ(models.Model):
    author = models.CharField(max_length=20)
    commentBody = models.CharField(default="", max_length=1000)
    pyq = models.ForeignKey(File, default=None, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.author

class CommentsExp(models.Model):
    author = models.CharField(max_length=20)
    commentBody = models.CharField(default="", max_length=1000)
    exp = models.ForeignKey(Interview, default=None, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.author        
