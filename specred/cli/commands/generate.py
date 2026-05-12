import os
from typing import Optional

import typer

from specred.agents.analyzer import analyze
from specred.agents.domain_agent import DomainAgent
from specred.agents.testgen_agent import TestGenAgent
from specred.agents.usecase_agent import UsecaseAgent
from specred.providers.base import ProviderError
from specred.providers.factory import create_provider
from specred.utils.filesystem import read_global_config, read_project_config


def _load_config() -> dict:
    config = read_global_config()
    if not config:
        typer.echo("설정 파일이 없습니다. 먼저 `specred init`을 실행하세요.", err=True)
        raise typer.Exit(1)
    return config


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
    if not os.path.exists(requirement):
        typer.echo(f"파일을 찾을 수 없습니다: {requirement}", err=True)
        raise typer.Exit(1)

    config = _load_config()
    project_config = read_project_config()
    test_config = project_config.get("test", {})

    provider_name = config.get("provider", "")
    api_key = config.get("api_key", "")
    resolved_model = model or config.get("model", "")

    if not provider_name or not api_key:
        typer.echo("provider 또는 api_key가 설정되지 않았습니다. `specred init`을 다시 실행하세요.", err=True)
        raise typer.Exit(1)

    resolved_lang = lang or test_config.get("language", "java")
    resolved_framework = framework or test_config.get("framework", "junit5")
    resolved_style = style or test_config.get("style", "behavior")
    coverage_target = project_config.get("coverage_target", test_config.get("coverage_target", 90))
    extra_rules = project_config.get("rules", test_config.get("rules", []))

    provider = create_provider(provider=provider_name, api_key=api_key, model=resolved_model)

    typer.echo("[1/4] 요구사항 분석 중...")
    analyzer_result = analyze(requirement)

    usecase_agent = UsecaseAgent(provider=provider)

    while True:
        typer.echo("[2/4] 유즈케이스 생성 중...")
        try:
            usecase_agent.run(analyzer_result)
        except ProviderError as e:
            typer.echo(f"오류: {e}", err=True)
            raise typer.Exit(1)

        typer.echo("\n✓ usecase.md 생성 완료\n")
        typer.echo("usecase.md를 확인하세요.")
        choice = typer.prompt("계속하려면 [o], 재생성하려면 [r], 종료하려면 [q]").strip().lower()

        if choice == "o":
            break
        elif choice == "r":
            typer.echo("")
            continue
        elif choice == "q":
            raise typer.Exit(0)
        else:
            typer.echo("o, r, q 중 하나를 입력하세요.")

    domain_agent = DomainAgent(provider=provider)

    while True:
        typer.echo("\n[3/4] 도메인 모델 추출 중...")
        try:
            domain_agent.run()
        except ProviderError as e:
            typer.echo(f"오류: {e}", err=True)
            raise typer.Exit(1)

        typer.echo("\n✓ domain.yml 생성 완료\n")
        typer.echo("domain.yml을 확인하세요.")
        choice = typer.prompt("계속하려면 [o], 재생성하려면 [r], 종료하려면 [q]").strip().lower()

        if choice == "o":
            break
        elif choice == "r":
            typer.echo("")
            continue
        elif choice == "q":
            raise typer.Exit(0)
        else:
            typer.echo("o, r, q 중 하나를 입력하세요.")

    testgen_agent = TestGenAgent(
        provider=provider,
        language=resolved_lang,
        framework=resolved_framework,
        style=resolved_style,
        coverage_target=coverage_target,
        rules=extra_rules,
    )

    while True:
        typer.echo(f"\n[4/4] 테스트 코드 생성 중... ({resolved_lang}/{resolved_framework}/{resolved_style})")
        try:
            generated_files = testgen_agent.run()
        except ProviderError as e:
            typer.echo(f"오류: {e}", err=True)
            raise typer.Exit(1)

        typer.echo("\n✓ 테스트 코드 생성 완료\n")

        if generated_files:
            typer.echo("생성된 파일:")
            for f in generated_files:
                typer.echo(f"  {f}")
        else:
            typer.echo("(생성된 파일 없음)")

        typer.echo("")
        choice = typer.prompt("계속하려면 [o], 재생성하려면 [r], 종료하려면 [q]").strip().lower()

        if choice == "o":
            typer.echo("완료.")
            break
        elif choice == "r":
            typer.echo("")
            continue
        elif choice == "q":
            raise typer.Exit(0)
        else:
            typer.echo("o, r, q 중 하나를 입력하세요.")
