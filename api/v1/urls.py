from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import FurnitureViewSet, RoomCopyView, RoomViewSet, SendPDFView

router = DefaultRouter()
router.register('furniture', FurnitureViewSet, basename='furniture')
router.register('rooms', RoomViewSet, basename='room')

urlpatterns = [
    path(r'rooms/send_email/', SendPDFView.as_view()),
    path(r'rooms/<int:pk>/', RoomCopyView.as_view()),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
