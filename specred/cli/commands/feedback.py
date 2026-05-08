import typer

# TODO: Orchestrator에 피드백 전달
# TODO: Orchestrator가 영향 범위를 판단해 필요한 에이전트만 호출
# TODO: 테스트 코드와 specred-report.md 함께 업데이트


def feedback(message: str = typer.Argument(..., help="변경사항 지시 (예: '동시 가입 테스트 추가해줘')")) -> None:
    """변경사항을 반영합니다."""
    # TODO: implement
    typer.echo(f"feedback: not implemented yet (message={message!r})")
