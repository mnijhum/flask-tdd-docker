class BaseConfig:
    TESTING = False


class DevelopmentConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    TESTING = False
    
class ProductionConfig(BaseConfig):
    pass

