from rest_framework.routers import DefaultRouter
from .views import ElectricalServiceViewSet,PaintingServiceViewSet,FlooringServiceViewSet

router = DefaultRouter()
router.register(r'electrical-services', ElectricalServiceViewSet, basename='electricalservice')
router.register(r'painting-services', PaintingServiceViewSet)
router.register(r'flooring-services',FlooringServiceViewSet)

urlpatterns = router.urls