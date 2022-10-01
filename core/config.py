from pydantic import BaseSettings


class Base(BaseSettings):
    class Config:
        env_file = './.env'


class AppSettings(Base):
    APP_PORT: int
    API_URL: str
    API_PATH: str
    API_VERSION: str
    SWAGGER_PATH: str
    SECRET_KEY: str


class DBSettings(Base):
    SCHEMA_NAME: str
    DRIVER: str
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    NAME: str

    class Config:
        env_prefix = 'DB_'


class Config(BaseSettings):
    APP: AppSettings = AppSettings()
    DB: DBSettings = DBSettings()


CONFIG = Config()


class InteractionConfig():
    SQLALCHEMY_DATABASE_URI = (
        f'{CONFIG.DB.DRIVER}://{CONFIG.DB.USER}:{CONFIG.DB.PASSWORD}'
        f'@{CONFIG.DB.HOST}:{CONFIG.DB.PORT}/{CONFIG.DB.NAME}'
    )


INTERACTION_CONFIG = InteractionConfig()
