
# if we want to load configuration from environment variables or a .env file we can use pydantic-settings to manage our settings. 
   

from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int
    model_config = SettingsConfigDict(

        env_file=".env",
        extra="ignore"
    )

# HERE we create an instance of the Settings class to access the configuration values throughout the application.
Config = Settings()
