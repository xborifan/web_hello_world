from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASS: str
    POSTGRES_DB: str
    
    JWT_SECRET_KEY: str = ""
    JWT_SECRET_ALG: str = ""
    TOKEN_BEARER: str = ""
    
    @property
    def databaseUrl(self):
        user = f"{self.POSTGRES_USER}:{self.POSTGRES_PASS}"
        db = f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return f"postgresql+asyncpg://{user}@{db}"
    
    
    class Config:
        env_file = ".env"
    
    
settings = Settings()    

print(settings.databaseUrl)
