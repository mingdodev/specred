import re

from specred.providers.base import LLMProvider
from specred.utils.filesystem import write_file

SYSTEM_PROMPT = """\
당신은 소프트웨어 요구사항 분석 전문가입니다.
요구사항을 읽고 Mermaid flowchart 다이어그램을 생성합니다.

규칙:
1. 반드시 아래 형식으로 시작할 것:
   flowchart LR
2. %%{init}%% 블록, 백틱(```), 마크다운 코드블록 절대 포함하지 말 것
3. 노드 ID는 영문+숫자만 사용 (UC_Signup, UC_Login 등)
4. 노드 라벨([] 안)은 한글 가능하지만 줄바꿈(\\n) 사용 금지
5. subgraph 이름은 큰따옴표로 감쌀 것
6. <<include>>, <<extend>> 표기 사용 금지
   - include 관계는 점선 화살표로: UC_A -.-> UC_B
   - extend 관계는 일반 화살표로: UC_A --> UC_B
7. actor는 사각형 노드로 표현: User[사용자]

출력은 Mermaid 코드만, 설명 없이.\
"""

OUTPUT_PATH = "usecase.md"


class UsecaseAgent:
    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider

    def run(self, analyzer_result: dict) -> str:
        """analyzer 결과를 받아 LLM을 호출하고 usecase.md를 생성한다."""
        raw_text = analyzer_result["raw_text"]
        user_message = f"다음 요구사항을 분석하여 Mermaid usecase diagram을 생성해줘:\n\n{raw_text}"

        response = self._provider.complete(system=SYSTEM_PROMPT, user=user_message)

        mermaid_code = _extract_mermaid(response)
        write_file(OUTPUT_PATH, f"```mermaid\n{mermaid_code}\n```")
        return OUTPUT_PATH


def _extract_mermaid(text: str) -> str:
    """응답에서 Mermaid 코드만 추출한다. 코드블록으로 감싸진 경우도 처리."""
    match = re.search(r"```(?:mermaid)?\s*\n?(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()
