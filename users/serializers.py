from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer

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
            "email",
            "birthday",
            "city",
            "i_am_designer",
            "password",
        )

    def update(self, instance, validated_data):
        user = self.context["request"].user
        if user.is_superuser or user == instance:
            instance.city = validated_data.get("city", instance.city)
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
