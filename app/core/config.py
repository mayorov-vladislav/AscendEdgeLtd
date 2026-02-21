from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:123456@127.0.0.1:5432/ascendedgeltd"

    model_config = {
        "env_file": ".env"
    }


settings = Settings()