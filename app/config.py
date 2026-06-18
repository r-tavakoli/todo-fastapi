from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSetting(BaseSettings):
    POSTGRE_SERVER: str
    POSTGRE_PORT: int
    POSTGRE_DB: str
    POSTGRE_USER_NAME: str
    POSTGRE_PASSWORD: str
    
    model_config = SettingsConfigDict(
        env_file = "./.env",
        env_ignore_empty = True,
        extra="ignore"
    )
    
    def POSTGRES_URL(self):
        return f"postgresql+ayncpg://{self.POSTGRE_USER_NAME}:{self.POSTGRE_PASSWORD}@{self.POSTGRE_SERVER}:{self.POSTGRE_PORT}/{self.POSTGRE_DB}"
    
setting = DatabaseSetting()
