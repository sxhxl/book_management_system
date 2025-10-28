from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@db:5432/bookdb"
    JWT_SECRET_KEY: str = "supersecretkey12345"
    OLLAMA_HOST: str = "http://ollama:11434"
    LLM_MODEL: str = "llama3.2:1b"

settings = Settings()
