from pydantic_settings import BaseSettings, SettingsConfigDict

_setting_config_dict = SettingsConfigDict(
        env_file = "./.env",
        env_ignore_empty = True,
        extra="ignore"
    )


class DatabaseSettings(BaseSettings):
    POSTGRE_SERVER: str
    POSTGRE_PORT: int
    POSTGRE_DB: str
    POSTGRE_USER_NAME: str
    POSTGRE_PASSWORD: str
    
    REDIS_SERVER: str
    REDIS_PORT: int
    REDIS_DB: int
    # REDIS_USER_NAME: str | None
    # REDIS_PASSWORD: str | None
    
    model_config = _setting_config_dict
    
    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRE_USER_NAME}:{self.POSTGRE_PASSWORD}@{self.POSTGRE_SERVER}:{self.POSTGRE_PORT}/{self.POSTGRE_DB}"

    @property
    def REDIS_URL(self):
        # connection_url = f"redis://{self.REDIS_USER_NAME}:{self.REDIS_PASSWORD}@{self.REDIS_SERVER}:{self.REDIS_PORT}/{self.REDIS_DB}"
        connection_url = f"redis://{self.REDIS_SERVER}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return connection_url
        
    
class SecuritySettings(BaseSettings):
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str       
    
    model_config = _setting_config_dict  
    
    
class NotificationSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str 
    MAIL_FROM: str
    MAIL_FROM_NAME: str 
    MAIL_SERVER: str 
    MAIL_PORT: int
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False 
    USE_CREDENTIALS: bool = True 
    VALIDATE_CERTS: bool = True
    
    model_config = _setting_config_dict      
        
db_settings = DatabaseSettings()
security_settings = SecuritySettings()
notification_settings = NotificationSettings()
