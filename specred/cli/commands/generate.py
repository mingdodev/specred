from typing import Optional
import typer

# TODO: Orchestrator를 호출해 요구사항 분석 → 유즈케이스 생성 → 도메인 확정 → 테스트 생성 전체 플로우 실행
# TODO: specred.yml이 없으면 테스트 스타일/언어/프레임워크 인터랙티브 질문
# TODO: --domain 플래그가 있으면 도메인 확정 단계 생략


def generate(
    requirement: str = typer.Option(..., "--requirement", "-r", help="요구사항 문서 경로 (필수)"),
    api_spec: Optional[str] = typer.Option(None, "--api-spec", help="API 스펙 파일 경로 (선택)"),
    domain: Optional[str] = typer.Option(None, "--domain", help="도메인 모델 문서 경로 (선택, 있으면 확정 단계 생략)"),
    model: Optional[str] = typer.Option(None, "--model", help="모델 오버라이드 (claude-opus-4-6 | claude-sonnet-4-6 | claude-haiku-4-5)"),
    style: Optional[str] = typer.Option(None, "--style", help="테스트 스타일 오버라이드 (behavior | describe)"),
    lang: Optional[str] = typer.Option(None, "--lang", help="언어 오버라이드 (java | kotlin | python | javascript)"),
    framework: Optional[str] = typer.Option(None, "--framework", help="프레임워크 오버라이드 (junit5 | kotest | pytest | jest)"),
) -> None:
    """요구사항 문서를 분석해 테스트 코드를 생성합니다."""
    # TODO: implement
    typer.echo("generate: not implemented yet")
