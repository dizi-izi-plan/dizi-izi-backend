from django.contrib.auth import get_user_model
from django.test import TestCase

from furniture import models

User = get_user_model()


class RoomLayoutTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="user@example.com",
            password="password",
        )
        cls.model_instance = models.RoomLayout.objects.create(
            user=cls.user,
            name="Гостиная",
            first_wall=3000,
            second_wall=4000,
            third_wall=3000,
            fourth_wall=4000,
        )

    def test_model_creation(self):
        """Тест создания объекта с валидными данными."""
        self.assertIsInstance(self.model_instance, models.RoomLayout)
        self.assertEqual(self.model_instance.user.email, "user@example.com")
        self.assertEqual(self.model_instance.name, "Гостиная")

    def test_str_representation(self):
        """Тест строкового представления объекта."""
        self.assertEqual(
            str(self.model_instance), "Проект Гостиная пользователя user@example.com"
        )
