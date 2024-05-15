from django.test import TestCase

from furniture import models


class RoomTypeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.model_instance = models.RoomType.objects.create(
            name="Гостиная", slug="living_room"
        )

    def test_model_creation(self):
        """Тест создания объекта с валидными данными."""
        self.assertIsInstance(self.model_instance, models.RoomType)
        self.assertEqual(self.model_instance.name, "Гостиная")

    def test_str_representation(self):
        """Тест строкового представления объекта."""
        self.assertEqual(str(self.model_instance), "living_room")


class FurnitureTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.room_type = models.RoomType.objects.create(
            name="Living Room",
        )
        cls.model_instance = models.Furniture.objects.create(
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

    def test_model_creation(self):
        """Тест создания объекта с валидными данными."""
        self.assertIsInstance(self.model_instance, models.Furniture)
        self.assertEqual(self.model_instance.name, "Стол")

    def test_str_representation(self):
        """Тест строкового представления объекта."""
        self.assertEqual(str(self.model_instance), "Стол")
