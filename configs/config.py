from os import getenv

class Config(object):
    SECRET_KEY = getenv('SECRET_KEY', 'I_got_the_strongest_secret_key')
    WTF_CSRF_SECRET_KEY = getenv('WTF_CSRF_SECRET_KEY', 'guess_if_you_can')
