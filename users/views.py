from djoser.views import UserViewSet

from users.serializers import CustomUserCreateSerializer


class UserView(UserViewSet):
    serializer_class = CustomUserAddSerializer

