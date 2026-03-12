from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "MyFastAPIApp"
    database_url: str = "postgresql://user:password@localhost:5432/mydb"
    secret_key: str = "test-secret"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

# Temporary test
# print(settings.app_name,'\n',settings.database_url,'\n',settings.secret_key)
