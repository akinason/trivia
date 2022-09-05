from collections import  namedtuple
import os
from pathlib import Path
from dotenv import dotenv_values

# Load environment variables from .env file then override the values with those located in the
# system environment variables.
config_dict = {
    **dotenv_values('.env'),
    **os.environ # Override loaded values with environment variables
}

config = {}
for k, v in config_dict.items():
    if k.startswith('_'):
        continue

    if k in ['FLASK_DEBUG', 'SQLALCHEMY_TRACK_MODIFICATIONS']:
        v = bool(v)

    config[k] = v

# Add specific variables.
config['BASE_DIR'] = Path(__file__).parent

# Create an object `settings` that will permit to call the environment variables using dot notation.
# e.g. >>> settings.FLASK_DEBUG
#      >>> settings.SQLALCHEMY_TRACK_MODIFICATIONS
settings = namedtuple('Settings', config.keys())(*config.values())
