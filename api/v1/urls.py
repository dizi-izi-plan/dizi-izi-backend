from django.urls import path, include

from .views import FurnitureViewSet, RoomViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('furniture', FurnitureViewSet, basename='furniture')
router.register('rooms', RoomViewSet, basename='room')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
