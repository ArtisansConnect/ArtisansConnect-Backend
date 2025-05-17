from django.urls import path
from .views import (
    PlanificationListViewManager,
    RefuseProject,
    ManagerListProject
)

urlpatterns = [
    path('project/',ManagerListProject.as_view()),
    path('project/state/<int:pk>/',RefuseProject.as_view()),
    path('planification/',PlanificationListViewManager.as_view())
]