"""
Validators are used in validation parameters, in the AUTH_PASSWORD_VALIDATORS constant in the settings module

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "validators.YourValidator",
        "OPTIONS": {
            "your_parameter": value
            },
    },
]
"""

import re

from django.contrib.auth.password_validation import MinimumLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class SpecialCharsValidator:
    """
    Checks if at least one special character is present in the password.

    :param special_chars:
        String containing special characters to be checked.
        Default value = DEFAULT_SPECIAL_CHARS
    """
    DEFAULT_SPECIAL_CHARS = '!#$%&‘*+-/=?^_`{|}~,.;:'

    def __init__(self, special_chars=DEFAULT_SPECIAL_CHARS):
        self.special_chars = set(special_chars)

    def validate(self, password, user=None):
        if not any(char in self.special_chars for char in password):
            raise ValidationError(
                _("Password must contain at least one special character: %(special_chars)s"),
                code="password_no_special_chars",
                params={"special_chars": ''.join(self.special_chars)}
            )

    def get_help_text(self):
        return _("Your password must contain at least one special character: %s") % ''.join(self.special_chars)


class LengthValidator(MinimumLengthValidator):
    """
    Extends the base validation class MinimumLengthValidator by adding maximum length validation.

    :param min_length:
        Minimum password length. Default value =  8
    :param max_length:
        Maximum password length. Default value = 128
    """

    def __init__(self, min_length=8, max_length=128):
        super().__init__(min_length=min_length)
        self.max_length = max_length

    def validate(self, password, user=None):
        super().validate(password)

        if len(password) > self.max_length:
            raise ValidationError(
                _("Password must contain no more than %(max_length)d chars."),
                code='password_too_long',
                params={"max_length": self.max_length},
            )

    def get_help_text(self):
        return _("Your password must be between %d and %d chars long.") % (self.min_length, self.max_length)


class AllowedCharsValidator:
    """
    Checks that only valid characters are used in the password

    :param special_chars:
        String containing special characters to be checked.
        Default value = DEFAULT_SPECIAL_CHARS
    """

    DEFAULT_SPECIAL_CHARS = '!#$%&‘*+-/=?^_`{|}~,.;:'

    def __init__(self, special_chars=DEFAULT_SPECIAL_CHARS):
        self.special_chars = special_chars
        self.password_pattern = rf'^[A-Za-z0-9{re.escape(self.special_chars)}]+$'
        self.password_regex = re.compile(self.password_pattern)

    def validate(self, password, user=None):
        if not self.password_regex.match(password):
            raise ValidationError(
                _("Password can contain only Latin letters, numbers, special chars: %(special_chars)s"),
                code='invalid_chas',
                params={'special_chars': self.special_chars},
            )

    def get_help_text(self):
        return _("Password can contain only Latin letters, numbers, special chars: %s") % self.special_chars


class HasUpperAndLowerCaseValidator:
    """
    Checks that the password has at least one uppercase and one lowercase letter
    """

    def validate(self, password, user=None):
        errors = []
        if not re.search(r'[A-Z]', password):
            errors.append(ValidationError(
                _("The password must contain at least one capital letter."),
                code='no_uppercase'
            ))
        if not re.search(r'[a-z]', password):
            errors.append(ValidationError(
                _("The password must contain at least one lowercase letter."),
                code='no_lowercase'
            ))
        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        return _("Your password must contain at least one capital letter and one lowercase letter.")


class HasDigitValidator:
    """
    Checks that the password contains at least one digit
    """

    def validate(self, password, user=None):
        if not re.search(r'[0-9]', password):
            raise ValidationError(
                _("The password must contain at least one digit"),
                code='no_digit'
            )

    def get_help_text(self):
        return _("Your password must contain at least one digit")
