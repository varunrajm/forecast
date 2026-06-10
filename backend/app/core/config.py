from functools import lru_cache
import os
from pathlib import Path
from tempfile import gettempdir

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Forecasta API"
    api_prefix: str = "/api"
    allowed_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    database_path: Path = Path(gettempdir()) / "forecasta" / "forecasta.db"
    upload_dir: Path = Path("uploads")

    model_config = {"env_prefix": "FORECASTA_"}


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.database_path.parent.mkdir(parents=True, exist_ok=True)
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    matplotlib_cache = Path(gettempdir()) / "forecasta" / "matplotlib"
    matplotlib_cache.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(matplotlib_cache))
    return settings
