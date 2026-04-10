from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "dominai trader journal"
    api_prefix: str = "/api"
    database_url: str = "postgresql+psycopg2://postgres:postgres@db:5432/trader"
    cors_origins: str = "http://localhost:3000"
    default_user_email: str = "demo@example.com"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
