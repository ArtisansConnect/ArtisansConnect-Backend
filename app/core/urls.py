from rest_framework.routers import DefaultRouter
from .views import ElectricalServiceViewSet

router = DefaultRouter()
router.register(r'electrical-services', ElectricalServiceViewSet, basename='electricalservice')

urlpatterns = router.urls