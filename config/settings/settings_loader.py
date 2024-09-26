"""
Module for dynamically loading Django settings based on the environment variable.

This module loads environment variables from a .env file and determines
which Django settings module to use based on the value of the
environment variable `PATH_TO_SETTINGS_MODULE`. If the variable is not set,
the default module `config.settings.base` is used.

Used environment variables:
- PATH_TO_SETTINGS_MODULE: Path to the Django settings module. ("config.settings.develop")

Exceptions:
- ImportError: Raised if the specified settings module is not found.
"""

import importlib
import os

from dotenv import load_dotenv

load_dotenv()

from .base import *  # noqa: F403, F401, E402

setting_module = os.getenv('PATH_TO_SETTINGS_MODULE', 'config.settings.prod')

try:
    import_settings_module = importlib.import_module(setting_module)
except ModuleNotFoundError as e:
    raise ImportError(
        f"Module '{setting_module}' not found. Ensure that the 'PATH_TO_SETTINGS_MODULE' variable "
        "is correctly set and the module is available for import."
    ) from e

globals().update(vars(import_settings_module))
