"""SCP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

from django.urls import path, include, re_path
from django.conf import settings
from SCPapp import views as s
from MockSchedularApp import views as m
from SCPapp import views
from django.conf.urls.static import static
from VideoModule import views as VideoModuleViews
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('getData/', views.getData.as_view(), name="getData"),
    path('getData/<int:id>/', views.patchData.as_view(), name="getDataId"),
    path('postData/', views.postData.as_view(), name="postData"),
    path('patchData/<int:id>/', views.patchData.as_view(), name="patchData"),
    path('pyq/comments/<int:id>/', views.getPostCommentsPYQ.as_view(), name="pyqComments"),
    path('deleteData/<id>/', csrf_exempt(views.deleteData.as_view()), name="deleteData"),
    path('interviewData/<int:id>/', views.interviewDataId.as_view(), name="interviewDataId"),
    path('interviewData/', views.interviewData.as_view(), name="interviewData"),
    path('exp/comments/<int:id>/', views.getPostCommentsExp.as_view(), name="expCommentsId"),
    
    path('getVideoData/', VideoModuleViews.getData.as_view(), name="getVideoData"),
    path('getVideoData/<int:id>/', VideoModuleViews.getDataById.as_view(), name="getVideoDataId"),
    path('postVideoData/', VideoModuleViews.postData.as_view(), name="postVideoData"),
    path('deleteVideoData/<int:id>/', csrf_exempt(VideoModuleViews.deleteData.as_view()), name="deleteVideoData"),
    path('updateVideoData/<int:id>/', VideoModuleViews.updateData.as_view(), name="updateVideoData"),
    path('commentsOnVideo/<int:id>/', VideoModuleViews.getPostComments.as_view(), name="commentsOnVideo"),

    re_path(r'^api/students/$', m.students_list),
    re_path(r'^api/students/([0-9]+)$', m.students_detail),
    re_path(r'^api/students/sendmail/([0-9]+)$', m.sendmail),

    path('token-auth/', obtain_jwt_token),
    path('loginData/', include('SCPapp.urls')),
    path('interviewData/admin/', views.interviewAdminView, name="interviewDataAdmin"),
    path('pyq/admin/', views.pyqAdminView, name="pyqAdmin"),
    path('video/admin/', VideoModuleViews.videoAdminView, name="videoAdmin"),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_set/', auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),

    path('confirmEmailID/', views.confirmEmailID.as_view(), name="confirmEmailID"),
    path('confirmEmailID/<int:otp>/', views.confirmEmailID.as_view(), name="confirmEmailID"),
    path('verifyEmailID/', views.verifyEmailID.as_view(), name="verifyEmailID"),

]


if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
