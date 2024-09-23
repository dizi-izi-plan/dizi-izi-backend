import os
from dotenv import load_dotenv
import importlib

# Loading environment variables and checking the variable PATH_TO_SETTINGS_MODULE
load_dotenv()
setting_module = os.getenv('PATH_TO_SETTINGS_MODULE', 'config.settings.base')

# Dynamic import of the settings module
import_settings_module = importlib.import_module(setting_module)

# Adding all variables from the imported module to the global viewport
globals().update(vars(import_settings_module))

