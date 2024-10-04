import re
from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, MaxValueValidator
from django.utils.regex_helper import _lazy_re_compile
from django.utils.translation import gettext as _


class PastDateValidator(MaxValueValidator):
    """
    Валидатор, ограничивающий дату текущим днем (не позволяет будущие даты)
    """
    message = "Дата не может быть в будущем."

    def __init__(self):
        super().__init__(limit_value=date.today, message=self.message)


class CustomEmailValidator(EmailValidator):
    """Extension of standard mail verification"""

    basic_message = _("Enter a valid email address.")
    length_message = _(
        "Length of username email from 1 to 63, length of domain from 4 to 192 (max 63 between dots) characters."
    )
    chars_include_message = _("Username Email can include . - _ domain . - ")

    message = [basic_message, length_message, chars_include_message]

    user_regex = _lazy_re_compile(
        r"^(?!.*[._-]{2})[a-z0-9]([a-z0-9._-]{0,61}[a-z0-9])?\Z",
        re.IGNORECASE,
    )

    def __call__(self, value):
        if len(value) > 256:
            raise ValidationError(self.message)

        if len(value.rsplit("@", 1)[1]) > 192:
            raise ValidationError(self.message)

        super().__call__(value)
