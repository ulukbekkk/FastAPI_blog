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

class GeneralSettings(BaseSettings):
    root_path: str
    api_key: str
    local_filesystem_root: str
    project_name: str
    version: str

    jwt_access_secret_key: str
    jwt_refresh_secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int

    class Config:
        env_file = ".env"


general = GeneralSettings()