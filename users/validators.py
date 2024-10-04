from datetime import date

from django.core.validators import MaxValueValidator
from django.core.validators import EmailValidator

class PastDateValidator(MaxValueValidator):
    """
    Валидатор, ограничивающий дату текущим днем (не позволяет будущие даты)
    """
    message = "Дата не может быть в будущем."

    def __init__(self):
        super().__init__(limit_value=date.today, message=self.message)



class CustomEmailValidator(EmailValidator):
    """Extension of standard mail verification"""

    def __call__(self, value):
        super().__call__(value)
