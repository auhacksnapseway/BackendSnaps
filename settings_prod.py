from settings_base import *

from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['localhost']

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
