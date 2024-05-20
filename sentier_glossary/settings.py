from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    base_url: str = "https://api.g.sentier.dev/"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
