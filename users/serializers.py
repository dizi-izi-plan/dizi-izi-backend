# from datetime import time
# from typing import Dict, Union

from django.contrib.auth import get_user_model
# from django.contrib.auth.password_validation import validate_password
# from django.core import exceptions as django_exceptions
from djoser.serializers import UserCreateSerializer
# from rest_framework import serializers

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Сериализатор для создания пользователей. Расширяет стандартный сериализатор Djoser UserCreateSerializer.

    Примечание: В настоящий момент изменения не активированы для использования в проекте.
    """

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            "id",
            # "first_name",
            "email",
            # "birthday",
            # "city",
            # "is_designer",
            "password",
        )

    # def validate_empty_values(
    #     self, data: Dict[str, Union[str, int, bool, time]],
    # ):
    #     """Изменение в валидации пустого пароля.

    #     Пустой пароль при POST запросе теперь не вызывает ошибки валидации
    #     и не изменяет пароль пользователя в базе данных.

    #     Args:
    #         data: Cодержимое полей запроса.

    #     Result:
    #         True if validate passed, False if failed.

    #     """
    #     super().validate_empty_values(data)

    #     if (self.context["request"].method == "PATCH"
    #             and data.get("password") == ""):
    #         return True, data

    #     return False, data

    # def validate(self, attrs: Dict[str, Union[str, int, bool, time]]):
    #     """При PATCH запросе убираем валидацию, если пароль не задается.

    #     Необходимо для того, чтобы изменять данные без ввода пароля. Доступ
    #     обеспечивается токеном из context'a.

    #     Args:
    #         attrs: Cодержимое полей запроса.

    #     Returns:
    #         Валидированные значения полей.

    #     Raises:
    #         django_exceptions.ValidationError если валидация провалена.

    #     """
    #     user = User(**attrs)
    #     password = attrs.get("password")
    #     method = self.context["request"].method
    #     if method == "PATCH" and password or method != "PATCH":
    #         try:
    #             validate_password(password, user)
    #         except django_exceptions.ValidationError as e:
    #             serializer_error = serializers.as_serializer_error(e)
    #             raise serializers.ValidationError(
    #                 {"password": serializer_error["non_field_errors"]},
    #             )
    #         return attrs
    #     return attrs

    # def update(
    #     self,
    #     instance: User,
    #     validated_data: Dict[str, Union[str, int, bool, time]],
    # ):
    #     """Вносим изменения методом PATCH в данные пользователя.

    #     Args:
    #         instance: Исходный объект класса User.
    #         validated_data: Валидированные значения полей.

    #     Returns:
    #         Обновленный объект класса пользователя.

    #     Raises:
    #         serializers.ValidationError если обновлять данные пытается не сам
    #         владелец данных или не суперюзер.

    #     """
    #     user = self.context["request"].user
    #     if user.is_superuser or user == instance:
    #         instance.city = validated_data.get("city", instance.city)
    #         instance.first_name = validated_data.get(
    #             "first_name", instance.first_name,
    #         )
    #         instance.email = validated_data.get("email", instance.email)
    #         instance.is_designer = validated_data.get(
    #             "is_designer", instance.is_designer,
    #         )
    #         instance.birthday = validated_data.get(
    #             "birthday", instance.birthday,
    #         )
    #         if validated_data.get("password"):
    #             instance.set_password(validated_data["password"])
    #         instance.save()
    #         return instance

    #     raise serializers.ValidationError(
    #         "Вы не можете изменять данные других пользователей.",
    #     )
