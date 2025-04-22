from rest_framework.routers import DefaultRouter
from .views import ElectricalServiceViewSet,PaintingServiceViewSet

router = DefaultRouter()
router.register(r'electrical-services', ElectricalServiceViewSet, basename='electricalservice')
router.register(r'painting-services', PaintingServiceViewSet)

urlpatterns = router.urls