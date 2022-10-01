import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    class Config:
        env_file = '../.env'


class ApiSettings(Settings):
    URL: str = Field('http://localhost')
    PORT: str = Field(..., env='APP_PORT')
    API_PATH: str
    API_VERSION: str


class DatabaseSettings(Settings):
    USER: str
    PASSWORD: str
    DB_HOST: str = Field('localhost')
    PORT: int
    NAME: str
    SCHEMA_NAME: str

    class Config:
        env_prefix = 'DB_'

    def dsn(self):
        return {
            'dbname': self.NAME,
            'user': self.USER,
            'password': self.PASSWORD,
            'host': self.DB_HOST,
            'port': self.PORT,
        }


class Config(Settings):
    API: ApiSettings = ApiSettings()
    DB: DatabaseSettings = DatabaseSettings()
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))


CONFIG = Config()
