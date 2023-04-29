from django.urls import path, include

from .views import FurnitureViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('furniture', FurnitureViewSet, basename='furniture')

urlpatterns = [
    path('v1/', include(router.urls)),
]
