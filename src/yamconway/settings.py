import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR / ".env"
load_dotenv(dotenv_path)

ALIVE_CELL_CHAR = os.getenv("ALIVE_CELL_CHAR", "#")
EMPTY_CELL_CHAR = os.getenv("EMPTY_CELL_CHAR", " ")
NR_OF_NBRS_TO_STARVE: int = int(os.getenv("NR_OF_NBRS_TO_STARVE", 2))
NR_OF_NBRS_TO_CREATE: int = int(os.getenv("NR_OF_NBRS_TO_CREATE", 3))

# Example settings
# SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')
# DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')
# ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')


# Database example
# DATABASES = {
#     'default': {
#         'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
#         'NAME': os.getenv('DB_NAME', BASE_DIR / 'db.sqlite3'),
#         'USER': os.getenv('DB_USER', ''),
#         'PASSWORD': os.getenv('DB_PASSWORD', ''),
#         'HOST': os.getenv('DB_HOST', ''),
#         'PORT': os.getenv('DB_PORT', ''),
#     }
# }
