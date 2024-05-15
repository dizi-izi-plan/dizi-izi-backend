from django.test import TestCase

from furniture import models


class CoordinateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.model_instance = models.Coordinate.objects.create(x=100, y=200)

    def test_model_creation(self):
        """Тест создания объекта с валидными данными."""
        self.assertIsInstance(self.model_instance, models.Coordinate)
        self.assertEqual(self.model_instance.x, 100)

    def test_str_representation(self):
        """Тест строкового представления объекта."""
        self.assertEqual(str(self.model_instance), "x=100, y=200")
