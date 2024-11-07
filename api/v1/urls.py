# from traceback import print_tb

from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from furniture.views import (FurnitureViewSet, RoomCopyView, RoomViewSet,
                             SendPDFView)
from tariff.views import APIChangeTariff, APITariff
from users.views import UserViewSet

router = DefaultRouter()
router.register("furniture", FurnitureViewSet, basename="furniture")
router.register("rooms", RoomViewSet, basename="room")

users = DefaultRouter()
users.register("users", UserViewSet, basename="customuser")


urlpatterns = [
    path(r"rooms/send_email/", SendPDFView.as_view()),
    path(r"rooms/copy/<int:pk>/", RoomCopyView.as_view()),
    path("tariffs/", APITariff.as_view()),
    path("tariffs/<slug:name_english>/", APIChangeTariff.as_view()),
    path("auth/", include(users.urls)),
    path("auth/", include("djoser.urls.authtoken")),
    path("", include(router.urls)),
    re_path(r'^social_auth/', include('drf_social_oauth2.urls', namespace='drf')),

]
