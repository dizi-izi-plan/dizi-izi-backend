from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter


from furniture.views import (FurnitureViewSet, RoomCopyView, RoomViewSet, SendPDFView)
from tariff.views import APITariff, APIChangeTariff

router = DefaultRouter()
router.register('furniture', FurnitureViewSet, basename='furniture')
router.register('rooms', RoomViewSet, basename='room')

urlpatterns = [
    path(r'rooms/send_email/', SendPDFView.as_view()),
    path(r'rooms/<int:pk>/', RoomCopyView.as_view()),
    path('', include(router.urls)),
    path('tariffs/', APITariff.as_view()),
    path('tariffs/<slug:name_english>/', APIChangeTariff.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    re_path("", include("social_django.urls", namespace="social")),
]
