from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.response import Response

from users.serializers import CustomUserCreateSerializer
from users.services.logout_user import logout_user


class UserViewSet(DjoserUserViewSet):
    """
    Расширяет базовый Djoser UserViewSet для более тонкой настройки
    """

    serializer_class = CustomUserCreateSerializer

    # TODO: настроить троттлинг

    # throttle_scope = "low_request"

    # def get_throttles(self):
    #     """
    #     Устанавливает классы троттлинга для действия создания пользователя "create".
    #     """
    #     if self.action == "create":
    #         self.throttle_classes = [AnonRateThrottle, UserRateThrottle]
    #     return super().get_throttles()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if user == instance:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = user

        logout_user(instance)

        instance.is_active = False

        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
