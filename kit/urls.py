from django.conf.urls import url, include
from .views import *
from rest_framework import routers
router=routers.SimpleRouter()

router.register(r'resources', ResourceViewSet, basename='resources')
router.register(r'persons', PersonViewSet, basename='persons')
router.register(r'assets', AssetViewSet, basename='assets')
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'widgets', WidgetViewSet, basename='widgets')
router.register(r'one-to-one-projects', ProjectOneToOneViewSet, basename='one_to_one_projects')
router.register(r'many-to-one-projects', ProjectManyToOneViewSet, basename='many_to_one_projects')
router.register(r'slot-settings', SlotSettingViewSet, basename='slot_settings')
router.register(r'bookings', BookingViewSet, basename='bookings')
router.register(r'one-to-one-bookings', OneToOneBookingViewSet, basename='one_to_one_bookings')
router.register(r'many-to-one-bookings', ManyToOneBookingViewSet, basename='many_to_one_bookings')

urlpatterns = router.urls