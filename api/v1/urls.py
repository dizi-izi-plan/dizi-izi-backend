# from traceback import print_tb

from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from furniture.views import (FurnitureViewSet, RoomCopyView, RoomListViewSet,
                             RoomTypeViewSet, RoomViewSet, SendPDFView, RoomLayoutListView)
from tariff.views import APIChangeTariff, APITariff
from users.views import UserViewSet

router = DefaultRouter()
router.register("furniture", FurnitureViewSet, basename="furniture")
router.register("rooms", RoomViewSet, basename="room")
router.register("rooms_type", RoomTypeViewSet, basename="room_type")
router.register("rooms_list", RoomListViewSet, basename="room_list")

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
    path("", include("social_django.urls", namespace="social")),
    re_path(r"^social_auth/", include("drf_social_oauth2.urls", namespace="social_auth")),
    path("rooms/<int:room_id>/layouts/", RoomLayoutListView.as_view()),
]
