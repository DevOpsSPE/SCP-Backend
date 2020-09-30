from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import File,Interview,User,CommentsPYQ,CommentsExp, emailVerify

admin.site.register(File)
admin.site.register(Interview)
admin.site.register(User)
admin.site.register(CommentsPYQ)
admin.site.register(CommentsExp)
admin.site.register(emailVerify)

# Register your models here.
