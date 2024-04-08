from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str
    mongo_initdb_root_username: str
    mongo_initdb_root_password: str

    model_config = SettingsConfigDict(env_file='./.env', env_file_encoding='utf-8')


settings = Settings()
