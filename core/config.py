from dynaconf import Dynaconf

_settings = Dynaconf(
    settings_file=["config.yaml"],
)


class Settings:
    def __init__(self, db_name: str) -> None:
        self.db_name: str = db_name


settings = Settings(db_name=_settings.database.db_name)


