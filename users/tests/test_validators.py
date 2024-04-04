from django.test import TestCase
from datetime import date, timedelta
from django.core.exceptions import ValidationError

from users.validators import PastDateValidator


class PastDateValidatorTest(TestCase):
    def test_past_date(self):
        validator = PastDateValidator()
        past_date = date.today() - timedelta(days=2)
        try:
            validator(past_date)
        except ValidationError:
            self.fail("Ошибка: PastDateValidator вызвал ValidationError для даты в прошлом.")

    def test_present_date(self):
        validator = PastDateValidator()
        present_date = date.today()
        try:
            validator(present_date)
        except ValidationError:
            self.fail("Ошибка: PastDateValidator вызвал ValidationError для текущей даты.")

    def test_future_date(self):
        validator = PastDateValidator()
        future_date = date.today() + timedelta(days=2)
        with self.assertRaises(ValidationError):
            validator(future_date)
