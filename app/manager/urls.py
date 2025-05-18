from django.urls import path
from .views import (
    PlanificationView,
    PlanificationListViewManager,
    RefuseProject,
    ManagerListProject
)

urlpatterns = [
    path('project/',ManagerListProject.as_view(),name='project-list'),                                   # see all the projects
    path('project/<int:pk>/',ManagerListProject.as_view(),name='project-detail'),                        # see only one project using id
    path('planification/',PlanificationListViewManager.as_view(),name='planification-list'),             # see all the planifications
    path('planification/<int:pk>/',PlanificationListViewManager.as_view(),name='planification-detail'),  # see only one planification using id
    path('planification/accept/', PlanificationView.as_view(),name='accept=project'),                    # accept project to create a new planification
    path('planification/reject/', RefuseProject.as_view(),name='refuse-project'),                        # refuse project 
]