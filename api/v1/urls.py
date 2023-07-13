from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FurnitureViewSet, RoomCopyView, RoomViewSet, SendPDFView,
                    APITariff, APIChangeTariff)

router = DefaultRouter()
router.register('furniture', FurnitureViewSet, basename='furniture')
router.register('rooms', RoomViewSet, basename='room')

urlpatterns = [
    path(r'rooms/send_email/', SendPDFView.as_view()),
    path(r'rooms/<int:pk>/', RoomCopyView.as_view()),
    path('', include(router.urls)),
    path('tariffs/', APITariff.as_view()),
    path('tariffs/<pk>/', APIChangeTariff.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
