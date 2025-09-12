from faststream.rabbit import RabbitBroker
from pydantic_settings import BaseSettings
from urllib.parse import quote


class Settings(BaseSettings):
    """Класс глобальных настроек приложения
    
    """    
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASS: str
    POSTGRES_DB:   str
    
    MQ_HOST:     str
    MQ_PORT:     int
    MQ_USER:     str
    MQ_PASSWORD: str
    MQ_VHOST:    str
    
    REDIS_HOST: str
    REDIS_PORT: int

    JWT_SECRET_KEY: str = ""
    JWT_SECRET_ALG: str = ""
    TOKEN_BEARER:   str = ""
    
    @property
    def databaseUrl(self):
        """Строка подключения к БД
        
        """    
        user = f"{self.POSTGRES_USER}:{self.POSTGRES_PASS}"
        db = f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return f"postgresql+asyncpg://{user}@{db}"
    
    @property
    def mqUrl(self) -> str:
        user = f"{self.MQ_USER}:{quote(self.MQ_PASSWORD)}"
        server = f"{self.MQ_HOST}:{self.MQ_PORT}/{self.MQ_VHOST}"
        return f"amqp://{user}@{server}"
       
    @property
    def redisUrl(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"   
        
    class Config:
        env_file = ".env"
    
    
settings = Settings()
broker = RabbitBroker(settings.mqUrl)