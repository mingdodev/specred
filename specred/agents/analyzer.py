import os

from specred.utils.filesystem import read_file

SUPPORTED_EXTENSIONS = {".md", ".txt", ".yaml", ".yml"}


def analyze(source_path: str) -> dict:
    """요구사항 문서를 읽어 텍스트를 추출한다. Claude API 호출 없음."""
    _, ext = os.path.splitext(source_path)

    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"지원하지 않는 파일 형식입니다: {ext} (지원: {', '.join(SUPPORTED_EXTENSIONS)})")

    raw_text = read_file(source_path)
    return {"raw_text": raw_text, "source_path": os.path.abspath(source_path)}
