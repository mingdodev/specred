import re
from pathlib import Path

import yaml

from specred.providers.base import LLMProvider

SYSTEM_PROMPT = """\
당신은 소프트웨어 도메인 모델링 전문가입니다.
유즈케이스 다이어그램을 분석하여 핵심 도메인 엔티티와 속성을 추출합니다.
반드시 아래 YAML 형식만 출력하고 설명은 포함하지 마세요.

출력 형식:
entities:
  - name: User
    attributes:
      - id: Long
      - email: String
      - password: String
    behaviors:
      - signup()
      - login()
  - name: Order
    attributes:
      - id: Long
      - status: String
      - totalPrice: BigDecimal
    behaviors:
      - place()
      - cancel()

규칙:
1. 반드시 entities: 키로 시작할 것
2. 각 엔티티는 name, attributes, behaviors 필드를 가질 것
3. attributes는 "필드명: 타입" 형식으로 작성할 것
4. behaviors는 "메서드명()" 형식으로 작성할 것
5. 백틱(```) 또는 마크다운 코드블록 포함 가능 (파싱 시 제거됨)
6. YAML 외 설명 텍스트 절대 포함하지 말 것\
"""

OUTPUT_PATH = Path("domain.yml")
USECASE_PATH = Path("usecase.md")


class DomainAgent:
    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider

    def run(self) -> Path:
        """usecase.md를 읽어 LLM을 호출하고 domain.yml을 생성한다."""
        usecase_content = USECASE_PATH.read_text(encoding="utf-8")
        user_message = (
            f"다음 유즈케이스 다이어그램을 분석하여 도메인 모델을 domain.yml 형식으로 추출해줘:\n\n{usecase_content}"
        )

        response = self._provider.complete(system=SYSTEM_PROMPT, user=user_message)

        yaml_content = _extract_yaml(response)
        OUTPUT_PATH.write_text(yaml_content, encoding="utf-8")
        return OUTPUT_PATH


def _extract_yaml(text: str) -> str:
    """응답에서 YAML만 추출한다. 코드블록으로 감싸진 경우도 처리."""
    match = re.search(r"```(?:yaml)?\s*\n?(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()
