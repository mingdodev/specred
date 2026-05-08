from pathlib import Path

import typer
import yaml

app = typer.Typer(invoke_without_command=True)

GLOBAL_CONFIG_PATH = Path.home() / ".specred" / "config.yml"

PROJECT_CONFIG_TEMPLATE = """\
# 테스트 스타일을 선택하세요 (기본값: behavior)
# behavior: Given-When-Then 구조
# describe: describe/it 계층 구조
test:
  style: {style}

# 개발 언어 (기본값: java)
  language: {language}

# 테스트 프레임워크 (기본값: junit5)
# java: junit5 | kotlin: kotest | python: pytest | javascript: jest
  framework: {framework}

# 커버리지 목표 (기본값: 90)
# coverage_target: 90

# 기본 룰 (항상 적용됩니다)
# - 일대다/다대다 관계는 연관된 데이터 내용까지 검증한다
# - 모든 테스트는 외부 환경 없이 항상 실행 가능해야 한다
#     DB: 인메모리 DB(@Transactional 롤백), 외부 서비스: WireMock/Stub
# - 외부 서비스 호출은 Mock 단위 테스트를 기본으로 작성하고,
#     통합 테스트는 Sandbox/Stub 서버를 가정해 설계한다
#     실제 호출 가능 여부는 생성 중 개발자에게 확인한다
# - 트랜잭션이 있는 경우 롤백 시나리오를 반드시 테스트한다
# - Null, Empty, 경계값은 항상 테스트한다
# - 룰 적용 중 판단이 필요한 지점에서는 진행을 멈추고 개발자에게 역질문한다
#
# 추가 룰이 필요하면 자연어로 작성하세요:
# rules:
#   - "페이지네이션이 있는 경우 빈 페이지와 마지막 페이지를 테스트한다"
"""

PROVIDERS = ["gemini", "anthropic", "openai"]

DEFAULT_MODELS = {
    "gemini": ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
    "anthropic": ["claude-sonnet-4-6", "claude-opus-4-6", "claude-haiku-4-5"],
    "openai": ["gpt-4o", "gpt-4o-mini", "codex-mini"],
}

RECOMMENDED_MODEL = {
    "gemini": "gemini-2.0-flash",
    "anthropic": "claude-sonnet-4-6",
    "openai": "gpt-4o",
}

STYLES = ["behavior", "describe"]
LANGUAGES = ["java", "kotlin", "python", "javascript"]
FRAMEWORK_MAP = {
    "java": "junit5",
    "kotlin": "kotest",
    "python": "pytest",
    "javascript": "jest",
}


def _confirm_overwrite(path: Path) -> bool:
    return typer.confirm(f"{path} 이 이미 존재합니다. 덮어쓸까요?")


def _write_global_config(provider: str, model: str, api_key: str) -> None:
    GLOBAL_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    config = {"provider": provider, "model": model, "api_key": api_key}
    GLOBAL_CONFIG_PATH.write_text(yaml.dump(config, allow_unicode=True))
    typer.echo(f"  저장됨: {GLOBAL_CONFIG_PATH}")


def _write_project_config(style: str, language: str, framework: str) -> None:
    project_config_path = Path.cwd() / "specred.yml"
    content = PROJECT_CONFIG_TEMPLATE.format(style=style, language=language, framework=framework)
    project_config_path.write_text(content)
    typer.echo(f"  저장됨: {project_config_path}")


@app.callback()
def init() -> None:
    """설정 파일을 초기화합니다."""
    typer.echo("\nspecred init\n")

    # --- 전역 설정 (~/.specred/config.yml) ---
    typer.echo("[ 전역 설정 ] ~/.specred/config.yml")

    if GLOBAL_CONFIG_PATH.exists() and not _confirm_overwrite(GLOBAL_CONFIG_PATH):
        typer.echo("  건너뜀.")
    else:
        typer.echo("\n  LLM provider를 선택하세요:")
        for i, p in enumerate(PROVIDERS, 1):
            typer.echo(f"    {i}. {p}")
        provider_idx = typer.prompt("  번호 선택", default="1")
        try:
            provider = PROVIDERS[int(provider_idx) - 1]
        except (ValueError, IndexError):
            provider = PROVIDERS[0]

        models = DEFAULT_MODELS[provider]
        recommended = RECOMMENDED_MODEL[provider]
        typer.echo(f"\n  사용할 모델을 선택하세요:")
        for i, m in enumerate(models, 1):
            note = " (권장)" if m == recommended else ""
            typer.echo(f"    {i}. {m}{note}")
        model_idx = typer.prompt("  번호 선택", default="1")
        try:
            model = models[int(model_idx) - 1]
        except (ValueError, IndexError):
            model = models[0]

        api_key = typer.prompt(f"  {provider} API 키를 입력하세요")

        _write_global_config(provider=provider, model=model, api_key=api_key)

    # --- 프로젝트 설정 (./specred.yml) ---
    typer.echo("\n[ 프로젝트 설정 ] ./specred.yml")

    project_config_path = Path.cwd() / "specred.yml"
    if project_config_path.exists() and not _confirm_overwrite(project_config_path):
        typer.echo("  건너뜀.")
    else:
        typer.echo("\n  테스트 스타일을 선택하세요:")
        for i, s in enumerate(STYLES, 1):
            typer.echo(f"    {i}. {s}")
        style_idx = typer.prompt("  번호 선택", default="1")
        try:
            style = STYLES[int(style_idx) - 1]
        except (ValueError, IndexError):
            style = STYLES[0]

        typer.echo("\n  개발 언어를 선택하세요:")
        for i, lang in enumerate(LANGUAGES, 1):
            typer.echo(f"    {i}. {lang}")
        lang_idx = typer.prompt("  번호 선택", default="1")
        try:
            language = LANGUAGES[int(lang_idx) - 1]
        except (ValueError, IndexError):
            language = LANGUAGES[0]

        framework = FRAMEWORK_MAP[language]
        typer.echo(f"  프레임워크: {framework} (언어에 따라 자동 선택됨)")

        _write_project_config(style, language, framework)

    typer.echo("\n초기화 완료.")
