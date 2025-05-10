from rest_framework.routers import DefaultRouter
from .views import (ElectricalServiceViewSet,
                    PaintingServiceViewSet,
                    FlooringServiceViewSet,
                    HvacServiceViewSet,
                    PlumbingServiceViewSet,
                    WindowsDoorsServiceViewSet,
                    RoofingServiceViewSet,
                    ConstructionHouseServiceViewSet,
                    FacadeServiceViewSet,
                    ProjectViewSet)

router = DefaultRouter()
router.register(r'electrical-services', ElectricalServiceViewSet, basename='electricalservice')
router.register(r'painting-services', PaintingServiceViewSet)
router.register(r'flooring-services',FlooringServiceViewSet)
router.register(r'hvac-services',HvacServiceViewSet)
router.register(r'plumbing-service',PlumbingServiceViewSet)
router.register(r'windowsdoors-service',WindowsDoorsServiceViewSet)
router.register(r'roofing-service',RoofingServiceViewSet)
router.register(r'construction-house-service',ConstructionHouseServiceViewSet)
router.register(r'facade-service',FacadeServiceViewSet)
router.register(r'project',ProjectViewSet)

urlpatterns = router.urls