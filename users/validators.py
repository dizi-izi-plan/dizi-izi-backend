import re
from datetime import date

from django.core.validators import EmailValidator, MaxValueValidator
from django.utils.regex_helper import _lazy_re_compile

class PastDateValidator(MaxValueValidator):
    """
    Валидатор, ограничивающий дату текущим днем (не позволяет будущие даты)
    """
    message = "Дата не может быть в будущем."

    def __init__(self):
        super().__init__(limit_value=date.today, message=self.message)


class CustomEmailValidator(EmailValidator):
    """Extension of standard mail verification"""

    user_regex = _lazy_re_compile(
         r"^(?!.*[._-]{2})[a-z0-9]([a-z0-9._-]{0,61}[a-z0-9])?\Z",
        re.IGNORECASE,
    )

    # domain_regex = _lazy_re_compile(
    #     r"((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+)(?:[a-z]{2,63}(?<!-))\Z",
    #     re.IGNORECASE,
    # )

    def __call__(self, value):
        value = value.lower()
        super().__call__(value)
