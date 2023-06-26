from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import FurnitureViewSet, RoomCopyView, RoomViewSet

router = DefaultRouter()
router.register('furniture', FurnitureViewSet, basename='furniture')
router.register('rooms', RoomViewSet, basename='room')


urlpatterns = [
    path(r'rooms/<int:pk>/', RoomCopyView.as_view()),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
