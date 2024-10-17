import re
from datetime import date

from django.core.validators import EmailValidator, MaxValueValidator
from django.core.exceptions import ValidationError
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

    user_regex = _lazy_re_compile(
         r"^(?!.*[._-]{2})[a-z0-9]([a-z0-9._-]{0,61}[a-z0-9])?\Z",
        re.IGNORECASE,
    )

    def __call__(self, value):
        super().__call__(value)


class SpecialCharsValidator:

    DEFAULT_SPECIAL_CHARS = '!#$%&‘*+—/=?^_`{|}~,.;:'

    def __init__(self, special_chars=DEFAULT_SPECIAL_CHARS):
        self.special_chars = set(special_chars)

    def validate(self, password, user=None):
        if not any(char in self.special_chars for char in password):
            raise ValidationError(
                _("Password must contain at least one special character: %(special_chars)s"),
                code="password_no_special_chars",
                params= {"special_chars": ''.join(self.special_chars)},
            )

    def get_help_text(self):
        return _("Your password must contain at least one special character: %s") % ''.join(self.special_chars)


class MaximumLengthValidator:

    def __init__(self, max_length=128):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                _("Password must contain no more than %(max_length)d characters."),
                code='password_too_long',
                params={"max_length": self.max_length},
            )

    def get_help_text(self):
        return _("Your password must contain no more than %d characters.") % self.max_length

