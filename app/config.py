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
    
    model_config = _setting_config_dict
    
    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRE_USER_NAME}:{self.POSTGRE_PASSWORD}@{self.POSTGRE_SERVER}:{self.POSTGRE_PORT}/{self.POSTGRE_DB}"
    
    
class SecuritySettings(BaseSettings):
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str       
    
    model_config = _setting_config_dict  
        
db_settings = DatabaseSettings()
security_settings = SecuritySettings()
