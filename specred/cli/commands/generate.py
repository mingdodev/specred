from pathlib import Path
from typing import Optional

import typer
import yaml

from specred.agents.analyzer import analyze
from specred.agents.usecase_agent import UsecaseAgent
from specred.providers.base import ProviderError
from specred.providers.factory import create_provider

GLOBAL_CONFIG_PATH = Path.home() / ".specred" / "config.yml"


def _load_config() -> dict:
    if not GLOBAL_CONFIG_PATH.exists():
        typer.echo("설정 파일이 없습니다. 먼저 `specred init`을 실행하세요.", err=True)
        raise typer.Exit(1)
    return yaml.safe_load(GLOBAL_CONFIG_PATH.read_text(encoding="utf-8")) or {}


def generate(
    requirement: str = typer.Option(..., "--requirement", "-r", help="요구사항 문서 경로 (필수)"),
    api_spec: Optional[str] = typer.Option(None, "--api-spec", help="API 스펙 파일 경로 (선택)"),
    domain: Optional[str] = typer.Option(None, "--domain", help="도메인 모델 문서 경로 (선택, 있으면 확정 단계 생략)"),
    model: Optional[str] = typer.Option(None, "--model", help="모델 오버라이드"),
    style: Optional[str] = typer.Option(None, "--style", help="테스트 스타일 오버라이드 (behavior | describe)"),
    lang: Optional[str] = typer.Option(None, "--lang", help="언어 오버라이드 (java | kotlin | python | javascript)"),
    framework: Optional[str] = typer.Option(None, "--framework", help="프레임워크 오버라이드 (junit5 | kotest | pytest | jest)"),
) -> None:
    """요구사항 문서를 분석해 테스트 코드를 생성합니다."""
    if not Path(requirement).exists():
        typer.echo(f"파일을 찾을 수 없습니다: {requirement}", err=True)
        raise typer.Exit(1)

    config = _load_config()

    provider_name = config.get("provider", "")
    api_key = config.get("api_key", "")
    resolved_model = model or config.get("model", "")

    if not provider_name or not api_key:
        typer.echo("provider 또는 api_key가 설정되지 않았습니다. `specred init`을 다시 실행하세요.", err=True)
        raise typer.Exit(1)

    provider = create_provider(provider=provider_name, api_key=api_key, model=resolved_model)

    typer.echo("[1/2] 요구사항 분석 중...")
    analyzer_result = analyze(requirement)

    typer.echo("[2/2] 유즈케이스 생성 중...")
    agent = UsecaseAgent(provider=provider)
    try:
        output_path = agent.run(analyzer_result)
    except ProviderError as e:
        typer.echo(f"오류: {e}", err=True)
        raise typer.Exit(1)

    typer.echo(f"완료 → {output_path}")
