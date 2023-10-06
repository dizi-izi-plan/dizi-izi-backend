from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class UserViewSet(DjoserUserViewSet):
    """Только для настройки троттлинга."""
    throttle_scope = 'low_request'

    def get_throttles(self):
        if self.action == "create":
            self.throttle_classes = [AnonRateThrottle, UserRateThrottle, ]
        return super().get_throttles()
