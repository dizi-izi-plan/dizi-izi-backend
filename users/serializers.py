from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from djoser.serializers import UserCreateSerializer
from django.core import exceptions as django_exceptions
from rest_framework import serializers

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            "id",
            "first_name",
            "email",
            "birthday",
            "city",
            "i_am_designer",
            "password",
        )

    def validate(self, attrs):
        """При PATCH запросе убираем валидацию, если пароль не задается."""
        user = User(**attrs)
        password = attrs.get("password")
        method = self.context["request"].method
        if method == "PATCH" and password or method != "PATCH":
            try:
                validate_password(password, user)
            except django_exceptions.ValidationError as e:
                serializer_error = serializers.as_serializer_error(e)
                raise serializers.ValidationError(
                    {"password": serializer_error["non_field_errors"]}
                )

            return attrs

        return attrs

    def update(self, instance, validated_data):
        user = self.context["request"].user
        if user.is_superuser or user == instance:
            instance.city = validated_data.get("city", instance.city)
            instance.first_name = validated_data.get("first_name", instance.first_name)
            instance.email = validated_data.get("email", instance.email)
            instance.i_am_designer = validated_data.get(
                "i_am_designer", instance.i_am_designer
            )
            instance.birthday = validated_data.get(
                "birthday", instance.birthday
            )
            if validated_data.get("password"):
                instance.set_password(validated_data["password"])
            instance.save()
            return instance
        else:
            raise serializers.ValidationError(
                "Вы не можете изменять данные других пользователей."
            )
