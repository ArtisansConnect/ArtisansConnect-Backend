from django.urls import path
from .views import (
    RequestRecrutement,
    UpdateArtisanProfile
)

urlpatterns = [
    path('recrutement/request/',RequestRecrutement.as_view(),name='request-recrutement'),
    path('profile/update/',UpdateArtisanProfile.as_view(),name='update-profile')
]