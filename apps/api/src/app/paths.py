from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def synthetic_root(data_root: Path | None = None) -> Path:
    root = data_root if data_root is not None else repo_root()
    return root / "data" / "synthetic"
