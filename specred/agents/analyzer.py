from pathlib import Path

SUPPORTED_EXTENSIONS = {".md", ".txt", ".yaml", ".yml"}


def analyze(source_path: str) -> dict:
    """요구사항 문서를 읽어 텍스트를 추출한다. Claude API 호출 없음."""
    path = Path(source_path)

    if not path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {source_path}")

    if path.suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"지원하지 않는 파일 형식입니다: {path.suffix} (지원: {', '.join(SUPPORTED_EXTENSIONS)})")

    raw_text = path.read_text(encoding="utf-8")
    return {"raw_text": raw_text, "source_path": str(path.resolve())}
