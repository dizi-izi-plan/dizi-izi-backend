from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from djoser.compat import get_user_email, get_user_email_field_name
from django.core import exceptions as django_exceptions
from djoser.serializers import UserCreateSerializer, UserSerializer

from djoser.conf import settings
from rest_framework import serializers

User = get_user_model()


class CustomUserCreateSerializer(UserSerializer):
    password = serializers.CharField(style={"input_type": "password"},
                                     write_only=True)
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = (settings.LOGIN_FIELD,)

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs
