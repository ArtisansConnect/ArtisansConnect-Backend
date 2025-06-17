from django.urls import path
from .views import UserListView,UserEditView,ProjectViewAdmin

urlpatterns = [
    path('users/',UserListView.as_view()),
    path('users/edit/',UserEditView.as_view()),
    path('projects/',ProjectViewAdmin.as_view())
]