from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def complete(self, system: str, user: str) -> str:
        """system 프롬프트와 user 메시지를 받아 응답 텍스트를 반환한다."""


class ProviderError(Exception):
    """LLM provider 호출 중 발생한 에러를 감싸는 공통 예외."""
