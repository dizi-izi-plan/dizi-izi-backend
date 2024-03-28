from django.core.validators import MaxValueValidator
from datetime import date


class PastDateValidator(MaxValueValidator):
    """
    Валидатор, ограничивающий дату текущим днем (не позволяет будущие даты)
    """
    message = "Дата не может быть в будущем."

    def __init__(self):
        super().__init__(limit_value=date.today, message=self.message)
