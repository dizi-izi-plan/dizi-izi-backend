from django.urls import path, include

from .views import FurnitureViewSet, RoomViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('furniture', FurnitureViewSet, basename='furniture')
router.register('rooms', RoomViewSet, basename='room')

urlpatterns = [
    path('v1/', include(router.urls)),
]
