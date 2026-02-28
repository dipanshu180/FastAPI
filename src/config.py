
# if we want to load configuration from environment variables or a .env file we can use pydantic-settings to manage our settings. 
   

from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_URL:str = "redis://localhost:6379/0"
    REDIS_DB: int = 0 
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str 
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    DOMAIN: str = "localhost:8000"
  
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

# HERE we create an instance of the Settings class to access the configuration values throughout the application.
Config = Settings()

broker_url = Config.REDIS_URL
result_backend = Config.REDIS_URL
broker_connection_retry_on_startup = True