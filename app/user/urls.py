
from django.urls import path
from .views import Signup
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from user.views import (
    CustomTokenObtainPairView,
    UpdateProfile
    )

urlpatterns = [
    path('register/',view=Signup.as_view(),name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('update/',UpdateProfile.as_view())
]
