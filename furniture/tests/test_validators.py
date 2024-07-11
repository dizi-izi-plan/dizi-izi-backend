from django.core.exceptions import ValidationError
from django.test import TestCase

from furniture.validators import minimum_len_width_validator


class MinimumLenWidthValidatorTest(TestCase):
    def test_validator_with_valid_value(self):
        """Тест с допустимым значением, не должен вызывать исключений."""
        valid_value = 10  # Значительно выше минимального
        try:
            minimum_len_width_validator(valid_value)
        except ValidationError:
            self.fail("ValidationError was raised unexpectedly!")

    def test_validator_with_invalid_value(self):
        """Тест с недопустимым значением, должен вызвать ValidationError."""
        invalid_value = 0  # Меньше минимального
        with self.assertRaises(ValidationError) as context:
            minimum_len_width_validator(invalid_value)
        self.assertIn('Минимальное значение для длины и ширины равно 1', str(context.exception))

    def test_validator_at_boundary(self):
        """Тест точной границы, не должен вызывать исключений."""
        boundary_value = 1  # Минимальное допустимое значение
        try:
            minimum_len_width_validator(boundary_value)
        except ValidationError:
            self.fail("ValidationError was raised unexpectedly at the boundary value!")
