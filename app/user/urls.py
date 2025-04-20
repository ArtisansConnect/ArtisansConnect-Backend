
from django.urls import path
from .views import Signup
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    path('register/',view=Signup.as_view(),name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
