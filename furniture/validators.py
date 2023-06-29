from django.core.exceptions import ValidationError


def minimum_len_width_validator(value):
    """Проверка минимального значения для длины и ширины мебели."""
    min_value_len_width = 1
    if value < min_value_len_width:
        raise ValidationError(
            (
                f'Минимальное значение для длины '
                f'и ширины равно {min_value_len_width}'
            ),
        )
    return value
