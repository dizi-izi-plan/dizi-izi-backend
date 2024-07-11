from django.contrib.auth import get_user_model
from django.test import TestCase

from furniture import models

User = get_user_model()


class BaseSetup(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="user@example.com",
            password="password",
        )
        cls.room_layout = models.RoomLayout.objects.create(
            user=cls.user,
            name="Гостиная",
            first_wall=3000,
            second_wall=4000,
            third_wall=3000,
            fourth_wall=4000,
        )


class FurniturePlacementTest(BaseSetup):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.room_type = models.RoomType.objects.create(
            name="Living Room",
        )
        cls.furniture = models.Furniture.objects.create(
            name="Стол",
            name_english="Table",
            length=1200,
            width=600,
            length_access=1300,
            width_access=700,
            type_of_rooms=cls.room_type,
            power_socket_type="Type-C",
            first_power_socket_height=400,
            first_power_socket_width=300,
            second_power_socket_height=500,
            second_power_socket_width=350,
        )
        cls.model_instance = models.FurniturePlacement.objects.create(
            furniture=cls.furniture,
            room=cls.room_layout,
        )

    def test_model_creation(self):
        """Тест создания объекта с валидными данными."""
        self.assertIsInstance(self.model_instance, models.FurniturePlacement)
        self.assertEqual(self.model_instance.furniture.name, "Стол")
        self.assertEqual(self.model_instance.room.name, "Гостиная")

    def test_str_representation(self):
        """Тест строкового представления объекта."""
        self.assertEqual(
            str(self.model_instance),
            "Стол расположена в Проект Гостиная пользователя user@example.com",
        )


class PowerSocketPlacementTest(BaseSetup):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_instance = models.PowerSocketPlacement.objects.create(
            room=cls.room_layout,
        )

    def test_model_creation(self):
        """Тест создания объекта с валидными данными."""
        self.assertIsInstance(self.model_instance, models.PowerSocketPlacement)
        self.assertEqual(self.model_instance.room.name, "Гостиная")

    def test_str_representation(self):
        """Тест строкового представления объекта."""
        self.assertEqual(
            str(self.model_instance),
            "Розетка расположена в Проект Гостиная пользователя user@example.com",
        )


class DoorPlacementTest(BaseSetup):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_instance = models.DoorPlacement.objects.create(
            room=cls.room_layout,
            width=100,
            open_inside=False,
        )

    def test_model_creation(self):
        """Тест создания объекта с валидными данными."""
        self.assertIsInstance(self.model_instance, models.DoorPlacement)
        self.assertEqual(self.model_instance.room.name, "Гостиная")

    def test_str_representation(self):
        """Тест строкового представления объекта."""
        self.assertEqual(
            str(self.model_instance),
            "Дверь расположена в Проект Гостиная пользователя user@example.com",
        )


class WindowPlacementTest(BaseSetup):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_instance = models.WindowPlacement.objects.create(
            room=cls.room_layout,
            length=100,
            width=100,
        )

    def test_model_creation(self):
        """Тест создания объекта с валидными данными."""
        self.assertIsInstance(self.model_instance, models.WindowPlacement)
        self.assertEqual(self.model_instance.room.name, "Гостиная")

    def test_str_representation(self):
        """Тест строкового представления объекта."""
        self.assertEqual(
            str(self.model_instance),
            "Окно расположено в Проект Гостиная пользователя user@example.com",
        )
