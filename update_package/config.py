import os

base_dir = os.getcwd()
Path = os.path.join(base_dir,'test.shell')

class Config(object):
    SECRET_KEY = 'hard to guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'db/data-dev.sqlite')


class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'db/data-test.sqlite')


class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'db/data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductConfig,
    'default': DevelopmentConfig,
    'path' : Path
}
