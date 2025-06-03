from django.urls import path
from .views import (
    RequestRecrutement,
    UpdateArtisanProfile
)
from .views import (
    ListElectricalTasks, UpdateElectricalProgress,
    ListPaintingTasks, UpdatePaintingProgress,
    ListFlooringTasks, UpdateFlooringProgress,
    ListHvacTasks, UpdateHvacProgress,
    ListPlumbingTasks, UpdatePlumbingProgress,
    ListWindowsDoorsTasks, UpdateWindowsDoorsProgress,
    ListRoofingTasks, UpdateRoofingProgress,
    ListConstructionHouseTasks, UpdateConstructionHouseProgress,
    ListFacadeTasks, UpdateFacadeProgress,
)

urlpatterns = [
    path('recrutement/request/',RequestRecrutement.as_view(),name='request-recrutement'),
    path('profile/update/',UpdateArtisanProfile.as_view(),name='update-profile'),
     # Electrical
    path('tasks/electrical/', ListElectricalTasks.as_view(), name='list-electrical-tasks'),
    path('tasks/electrical/progress/<int:pk>/', UpdateElectricalProgress.as_view(), name='update-electrical-progress'),

    # Painting
    path('tasks/painting/', ListPaintingTasks.as_view(), name='list-painting-tasks'),
    path('tasks/painting/progress/<int:pk>/', UpdatePaintingProgress.as_view(), name='update-painting-progress'),

    # Flooring
    path('tasks/flooring/', ListFlooringTasks.as_view(), name='list-flooring-tasks'),
    path('tasks/flooring/progress/<int:pk>/', UpdateFlooringProgress.as_view(), name='update-flooring-progress'),

    # HVAC
    path('tasks/hvac/', ListHvacTasks.as_view(), name='list-hvac-tasks'),
    path('tasks/hvac/progress/<int:pk>/', UpdateHvacProgress.as_view(), name='update-hvac-progress'),

    # Plumbing
    path('tasks/plumbing/', ListPlumbingTasks.as_view(), name='list-plumbing-tasks'),
    path('tasks/plumbing/progress/<int:pk>/', UpdatePlumbingProgress.as_view(), name='update-plumbing-progress'),

    # Windows & Doors
    path('tasks/windows-doors/', ListWindowsDoorsTasks.as_view(), name='list-windows-doors-tasks'),
    path('tasks/windows-doors/progress/<int:pk>/', UpdateWindowsDoorsProgress.as_view(), name='update-windows-doors-progress'),

    # Roofing
    path('tasks/roofing/', ListRoofingTasks.as_view(), name='list-roofing-tasks'),
    path('tasks/roofing/progress/<int:pk>/', UpdateRoofingProgress.as_view(), name='update-roofing-progress'),

    # Construction House
    path('tasks/construction-house/', ListConstructionHouseTasks.as_view(), name='list-construction-house-tasks'),
    path('tasks/construction-house/progress/<int:pk>/', UpdateConstructionHouseProgress.as_view(), name='update-construction-house-progress'),

    # Facade
    path('tasks/facade/', ListFacadeTasks.as_view(), name='list-facade-tasks'),
    path('tasks/facade/progress/<int:pk>/', UpdateFacadeProgress.as_view(), name='update-facade-progress'),
]