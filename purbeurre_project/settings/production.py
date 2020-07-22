from . import *

SECRET_KEY = "=)#vyU^4UI8\r!2\x0c+=C\\H+~t|"
DEBUG = False
ALLOWED_HOSTS = ['164.90.215.179']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # on utilise l'adaptateur postgresql
        'NAME': 'purbeurre', # le nom de notre base de données créée précédemment
        'USER': 'raoof', # attention : remplacez par votre nom d'utilisateur !!
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
