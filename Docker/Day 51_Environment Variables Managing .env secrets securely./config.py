from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str
    database_url: str
    secret_key: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

# Temporary test
# print(settings.app_name,'\n',settings.database_url,'\n',settings.secret_key)