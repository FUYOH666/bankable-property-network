import json
import logging
from pathlib import Path
from typing import Any

from app.paths import synthetic_root


logger = logging.getLogger(__name__)


class DataLoadError(Exception):
    def __init__(self, relative_path: str, reason: str) -> None:
        self.relative_path = relative_path
        self.reason = reason
        super().__init__(f"{relative_path}: {reason}")


def load_json(relative_path: str, *, base_dir: Path | None = None) -> dict[str, Any]:
    root = base_dir if base_dir is not None else synthetic_root()
    path = root / relative_path
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        logger.error("Synthetic data file missing path=%s", path)
        raise DataLoadError(relative_path, "file not found") from exc
    except json.JSONDecodeError as exc:
        logger.error("Synthetic data JSON invalid path=%s", path)
        raise DataLoadError(relative_path, "invalid JSON") from exc
