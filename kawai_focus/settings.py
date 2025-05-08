from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelConfig(BaseSettings):
    """Модель конфигурации"""

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )


class SettingsDB(ModelConfig):
    """Класс для данных БД"""

    name_db: str
    echo_db: bool

    @property
    def get_url_db(self) -> str:
        """Метод вернёт URL для подключения к БД"""

        return f'sqlite:///{self.name_db}'


class Settings(ModelConfig):
    """Класс для данных конфига"""

    db_settings: SettingsDB = SettingsDB()


settings = Settings()
