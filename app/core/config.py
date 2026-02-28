from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:123456@127.0.0.1:5432/ascendedgeltd"
    OPENAI_API_KEY: str

    model_config = {
        "env_file": ".env"
    }


settings = Settings()