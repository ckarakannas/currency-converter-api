class BaseConfig(object):
    DEBUG = False
    TESTING = False
    PROPAGATE_EXCEPTIONS = True


class ProductionConfig(BaseConfig):
    FLASK_ENV = 'production'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    FLASK_ENV = 'development'


class TestingConfig(BaseConfig):
    FLASK_ENV = 'development'
    TESTING = True
    DEBUG = True
