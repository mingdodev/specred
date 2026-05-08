import typer

from specred.cli.commands.init import app as init_app
from specred.cli.commands.generate import generate
from specred.cli.commands.review import review
from specred.cli.commands.feedback import feedback

app = typer.Typer(
    name="specred",
    help="자연어 요구사항을 BDD 시나리오로, 시나리오를 실행 가능한 테스트 코드로. TDD의 Red 단계를 자동화합니다.",
    no_args_is_help=True,
)

app.add_typer(init_app, name="init")
app.command("generate")(generate)
app.command("review")(review)
app.command("feedback")(feedback)

if __name__ == "__main__":
    app()
