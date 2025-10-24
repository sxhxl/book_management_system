from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/bookdb"
    JWT_SECRET_KEY: str = "supersecretkey"
    OLLAMA_HOST: str = "http://localhost:11434"
    LLM_MODEL: str = "llama3:8b"

settings = Settings()
