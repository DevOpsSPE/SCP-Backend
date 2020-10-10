from django.urls import path
from .views import *

urlpatterns = [
    path('current_user/', current_user),
    path('adminverify/', adminVerify),
    path('create/', UserList.as_view()),
    path('', UserList.as_view()),
    path('<rollNumber>/', loginDataId.as_view()),
]
