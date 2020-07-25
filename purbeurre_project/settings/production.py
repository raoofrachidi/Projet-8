from . import *

SECRET_KEY = 'gFIgQ%Llp2m{k^PC]z](y61+'
DEBUG = False
ALLOWED_HOSTS = ['139.59.140.175']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'purbeurre', 
        'USER': 'raoof', 
        'PASSWORD': 'password',
        'HOST': '',
        'PORT': '5432',
    }
}
