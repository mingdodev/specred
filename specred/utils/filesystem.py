from pathlib import Path

import yaml

_GLOBAL_CONFIG_PATH = Path.home() / ".specred" / "config.yml"
_PROJECT_CONFIG_PATH = Path("specred.yml")


def read_global_config() -> dict:
    if not _GLOBAL_CONFIG_PATH.exists():
        return {}
    return yaml.safe_load(_GLOBAL_CONFIG_PATH.read_text(encoding="utf-8")) or {}


def write_global_config(data: dict) -> None:
    _GLOBAL_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    _GLOBAL_CONFIG_PATH.write_text(yaml.dump(data, allow_unicode=True), encoding="utf-8")


def read_project_config() -> dict:
    if not _PROJECT_CONFIG_PATH.exists():
        return {}
    return yaml.safe_load(_PROJECT_CONFIG_PATH.read_text(encoding="utf-8")) or {}


def write_project_config(data: dict) -> None:
    _PROJECT_CONFIG_PATH.write_text(yaml.dump(data, allow_unicode=True), encoding="utf-8")


def read_file(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")
    return p.read_text(encoding="utf-8")


def write_file(path: str, content: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
