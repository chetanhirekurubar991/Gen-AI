from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_name:str ="My App"
    redis_host: str ="redis"
    redis_port : int = 6379

    model_config=SettingsConfigDict(env_file=".env")
settings=Settings()