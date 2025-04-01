from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    WORKERS_COUNT: int = 4
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    RELOAD: bool = True
    SECRET_KEY: str
    DATABASE_URL: str
    ASYNC_DATABASE_URL: str
    REDIS_URL: str
    ACCESS_SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ALGORITHM: str
    DEBUG: bool

    @property
    def taskiq_broker_url(self) -> str:
        return self.REDIS_URL

    @property
    def taskiq_result_backend_url(self) -> str:
        return self.REDIS_URL

    class Config:
        env_file = ".env"


settings = Settings()
