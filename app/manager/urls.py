from django.urls import path
from .views import (
    PlanificationView,
    PlanificationListViewManager,
    RefuseProject,
    ManagerListProject,
    TagView,
    BlogView,
    BlogListView,
    AcceptRecrutement,
    RejectRecrutement,
    ArtisanList,
    UpdateBlog,
    TagViewGeneral,
    ProjectArtisanAffectAPIView
)

urlpatterns = [
    # Client Side
    path('project/',ManagerListProject.as_view(),name='project-list'),                                   # see all the projects
    path('project/<int:pk>/',ManagerListProject.as_view(),name='project-detail'),                        # see only one project using id
    path('planification/',PlanificationListViewManager.as_view(),name='planification-list'),             # see all the planifications
    path('planification/<int:pk>/',PlanificationListViewManager.as_view(),name='planification-detail'),  # see only one planification using id
    path('planification/accept/', PlanificationView.as_view(),name='accept=project'),                    # accept project to create a new planification
    path('planification/reject/<int:pk>/', RefuseProject.as_view(),name='refuse-project'),               # refuse project 
    # General Side
    path('tags/',TagView.as_view(),name='tags-list'),
    path('tags/general/',TagViewGeneral.as_view(),name='tags-home'),
    path('blogs/',BlogListView.as_view(),name='blogs-list'),
    path('blogs/create/',BlogView.as_view(),name='blog'),
    path('blogs/update/<int:pk>/',UpdateBlog.as_view(),name='update-blog'),
    # Artisan Side
    path('hiring/accept/<int:pk>/',AcceptRecrutement.as_view(),name='accept-hiring'),                   # accept recrutement
    path('hiring/reject/<int:pk>/',RejectRecrutement.as_view(),name='accept-hiring'),                   # reject recrutement
    path('artisans/list/',ArtisanList.as_view(),name='artisan-list'),                                   # see all the artisans
    path('artisans/affect/<int:pk>/', ProjectArtisanAffectAPIView.as_view(), name='assign-artisans')
]