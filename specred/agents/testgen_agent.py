import re

import typer

from specred.providers.base import LLMProvider
from specred.utils.filesystem import read_file, write_file

DEFAULT_RULES = [
    "일대다/다대다 관계는 연관된 데이터 내용까지 검증한다",
    "모든 테스트는 외부 환경 없이 항상 실행 가능해야 한다",
    (
        "외부 서비스 호출은 Mock/Stub으로 격리하여 테스트한다\n"
        "    통합 테스트는 Sandbox/Stub 서버를 가정해 설계한다\n"
        "    실제 호출 가능 여부는 생성 중 개발자에게 확인한다"
    ),
    "트랜잭션이 있는 경우 롤백 시나리오를 반드시 테스트한다",
    "Null, Empty, 경계값은 항상 테스트한다",
    "룰 적용 중 판단이 필요한 지점에서는 진행을 멈추고 역질문한다",
]

USECASE_PATH = "usecase.md"
DOMAIN_PATH = "domain.yml"
MAX_RETRIES = 5


class TestGenAgent:
    def __init__(
        self,
        provider: LLMProvider,
        language: str,
        framework: str,
        style: str,
        coverage_target: int,
        rules: list[str],
    ) -> None:
        self._provider = provider
        self._language = language
        self._framework = framework
        self._style = style
        self._coverage_target = coverage_target
        all_rules = DEFAULT_RULES + (rules or [])
        self._rules_text = "\n".join(f"- {r}" for r in all_rules)
        self._style_guide = (
            "Given-When-Then 구조로 작성하세요."
            if style == "behavior"
            else "describe/it 계층 구조로 작성하세요."
        )

    def run(self) -> list[str]:
        """domain.yml과 usecase.md를 읽어 테스트 코드를 생성한다. 역질문 발생 시 개발자에게 확인 후 재시도."""
        usecase_content = read_file(USECASE_PATH)
        domain_content = read_file(DOMAIN_PATH)

        system = self._build_system_prompt()
        base_request = (
            "아래 도메인 모델과 유즈케이스를 바탕으로 테스트 코드를 생성하세요.\n\n"
            f"## domain.yml\n{domain_content}\n\n"
            f"## usecase.md\n{usecase_content}"
        )
        qa_context = ""

        for _ in range(MAX_RETRIES):
            response = self._provider.complete(system=system, user=base_request + qa_context)

            if response.strip().startswith("QUESTION:"):
                question = response.strip()[len("QUESTION:"):].strip()
                typer.echo(f"\n[질문] {question}")
                answer = typer.prompt("답변").strip()
                qa_context += (
                    f"\n\n[이전 질문과 답변]\nQ: {question}\nA: {answer}\n\n"
                    "위 답변을 반영하여 테스트 코드를 계속 생성하세요."
                )
            else:
                return _parse_and_save(response)

        typer.echo("최대 재시도 횟수를 초과했습니다.", err=True)
        return []

    def _build_system_prompt(self) -> str:
        return (
            f"당신은 {self._language}/{self._framework} 테스트 코드 작성 전문가입니다.\n"
            f"{self._style_guide}\n"
            f"커버리지 목표: {self._coverage_target}%\n\n"
            f"반드시 아래 룰을 적용하세요:\n{self._rules_text}\n\n"
            "도메인 모델과 유즈케이스를 분석하여 적절한 파일 구조를 스스로 판단하세요.\n"
            "구조가 명확하지 않거나 판단이 필요한 경우 QUESTION: 형식으로 개발자에게 확인하세요.\n\n"
            "판단이 필요한 지점이 생기면 코드 생성을 즉시 멈추고\n"
            "반드시 아래 형식으로만 응답하세요:\n"
            "QUESTION: <질문 내용>\n\n"
            "출력 형식:\n"
            f"### <파일 경로>\n"
            f"```{self._language}\n"
            "<코드>\n"
            "```\n"
            "파일이 여러 개면 위 형식을 반복하세요.\n"
            "설명은 포함하지 마세요."
        )


def _parse_and_save(response: str) -> list[str]:
    """### 파일경로 + 코드블록 패턴으로 파일을 분리하여 저장한다."""
    pattern = re.compile(r"###\s+(.+?)\n```(?:\w+)?\n(.*?)```", re.DOTALL)
    saved: list[str] = []

    for match in pattern.finditer(response):
        file_path = match.group(1).strip()
        code = match.group(2).rstrip()
        write_file(file_path, code)
        saved.append(file_path)

    return saved
