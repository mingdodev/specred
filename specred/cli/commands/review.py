import typer

# TODO: specred-report.md를 읽어 유즈케이스 커버리지 요약을 출력
# TODO: --docs 플래그 시 specred-report.md 생성 (DocWriter Agent 호출)


def review(
    docs: bool = typer.Option(False, "--docs", help="specred-report.md 생성"),
) -> None:
    """유즈케이스 커버리지 요약을 출력합니다."""
    # TODO: implement
    typer.echo("review: not implemented yet")
