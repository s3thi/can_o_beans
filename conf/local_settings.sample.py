LOCAL_SETTINGS = True
from settings import *

DEBUG = False

# For PostgreSQL.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'can_o_beans',
        'PASSWORD': '', 
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

STATIC_ROOT = "/home/web/static"SITE_ID = 1