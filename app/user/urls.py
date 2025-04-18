
from django.urls import path
from .views import Signup

urlpatterns = [
    path('register/',view=Signup.as_view(),name='register')
]
