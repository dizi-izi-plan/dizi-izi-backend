from datetime import datetime, timezone

from rest_framework import serializers

from tariff.models import Tariff, UsersTariffs


class TariffSerializer(serializers.ModelSerializer):
    # is_active = serializers.BooleanField(default=False, allow_null=True)
    is_active = serializers.SerializerMethodField()
    start_day = serializers.SerializerMethodField()
    period = serializers.SerializerMethodField()
    next_day_of_payment = serializers.SerializerMethodField()
    project_limit = serializers.IntegerField(default=0, allow_null=False)
    rooms_limit = serializers.IntegerField(default=0, allow_null=False)

    class Meta:
        model = Tariff
        fields = "__all__"

    def get_is_active(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return UsersTariffs.objects.filter(user=user, tariff=obj).exists()

    def get_start_day(self, obj):
        request = self.context.get("request")
        if not request.user.is_anonymous and not obj.is_active:
            user_tariff = obj.user_tariff.get(user=request.user)
            return user_tariff.start_date.strftime("%d.%m.%Y")

    def get_next_day_of_payment(self, obj):
        request = self.context.get("request")
        if not request.user.is_anonymous and not obj.is_active:
            user_tariff = obj.user_tariff.get(user=request.user)
            return (
                f'{user_tariff.start_date.strftime("%d")}.'
                f'{datetime.now(timezone.utc).strftime("%m")}'
            )

    def get_period(self, obj):
        return f"{obj.period.days} дней"


class ChangeTariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersTariffs
        fields = ("user", "tariff")
        read_only_fields = ("user", "tariff")

    def validate(self, data):
        tariff = self.initial_data.get("tariff")
        user = self.initial_data.get("user")
        if UsersTariffs.objects.filter(user=user, tariff=tariff).exists():
            raise serializers.ValidationError("У вас уже этот тариф.")
        return data
