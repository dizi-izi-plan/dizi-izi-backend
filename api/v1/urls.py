from django.urls import path, include

from .views import FurnitureViewSet, RoomViewSet, APITariff, APIChangeTariff

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('furniture', FurnitureViewSet, basename='furniture')
router.register('rooms', RoomViewSet, basename='room')
# router.register('tariffs', APITariff.as_view(), basename='tariff')
# router.register('tariffs/(?P<tariff_id>/d+)',
#                 APITariffDetail.as_view(), basename='change_tariff')

urlpatterns = [
    path('', include(router.urls)),
    path('tariffs/', APITariff.as_view()),
    path('tariffs/<pk>/', APIChangeTariff.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt'))
]
