from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from users.validators import PastDateValidator


class PastDateValidatorTest(TestCase):
    """
    Тесты для PastDateValidator.

    Валидатор проверяет, что заданная дата не превышает текущую дату,
    не позволяя использовать будущие даты.
    """
    def test_past_date(self):
        """Проверяет, что дата в прошлом не вызывает ошибку валидации."""
        validator = PastDateValidator()
        past_date = date.today() - timedelta(days=2)
        try:
            validator(past_date)
        except ValidationError:
            self.fail("Ошибка: PastDateValidator вызвал ValidationError для даты в прошлом.")

    def test_present_date(self):
        """Проверяет, что текущая дата не вызывает ошибку валидации."""
        validator = PastDateValidator()
        present_date = date.today()
        try:
            validator(present_date)
        except ValidationError:
            self.fail("Ошибка: PastDateValidator вызвал ValidationError для текущей даты.")

    def test_future_date(self):
        """Проверяет, что будущая дата вызывает ошибку валидации."""
        validator = PastDateValidator()
        future_date = date.today() + timedelta(days=2)
        with self.assertRaises(ValidationError):
            validator(future_date)
