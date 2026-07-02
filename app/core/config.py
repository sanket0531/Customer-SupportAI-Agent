from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str

    DATABASE_SERVER: str
    DATABASE_NAME: str
    DATABASE_DRIVER: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def DATABASE_URL(self) -> str:
        driver = quote_plus(self.DATABASE_DRIVER)

        return (
            f"mssql+pyodbc://@{self.DATABASE_SERVER}/{self.DATABASE_NAME}"
            f"?driver={driver}&trusted_connection=yes"
        )


settings = Settings()