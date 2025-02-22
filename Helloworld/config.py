import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'production'
    DEBUG = False
    TESTING = False 