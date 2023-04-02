from pydantic import BaseSettings


class DatabaseSettings(BaseSettings):
    driver: str = "postgresql+asyncpg"
    db: str
    user: str
    password: str
    host: str
    port: str
    echo: bool = False

    class Config:
        env_file = ".env"
        env_prefix = "postgres_"

    @property
    def uri(self) -> str:
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


database_settings = DatabaseSettings()