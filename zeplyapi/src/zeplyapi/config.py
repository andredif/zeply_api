from pydantic.env_settings import BaseSettings
from pydantic.fields import Field


class Settings(BaseSettings):
    ZEPLY_API_KEY: str = Field(..., env="ZEPLY_API_KEY")
    API_KEY_NAME: str = Field(..., env="API_KEY_NAME")
    ZEPLY_MNEMONIC_KEY: str = Field(..., env="ZEPLY_MNEMONIC_KEY")

    DB_USER : str = Field(..., env="POSTGRES_USER")
    DB_PASS : str = Field(..., env="POSTGRES_PASSWORD")
    DB_HOST : str = Field(..., env="POSTGRES_HOST")
    DB_PORT : str = Field(..., env="POSTGRES_PORT")


settings = Settings()
