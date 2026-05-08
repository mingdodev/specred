import anthropic

from specred.providers.base import LLMProvider, ProviderError


class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str, model: str) -> None:
        self._client = anthropic.Anthropic(api_key=api_key)
        self._model = model

    def complete(self, system: str, user: str) -> str:
        try:
            message = self._client.messages.create(
                model=self._model,
                max_tokens=4096,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
            return message.content[0].text
        except anthropic.AuthenticationError as e:
            raise ProviderError(f"Anthropic 인증 실패: API 키를 확인하세요. ({e})") from e
        except anthropic.RateLimitError as e:
            raise ProviderError(f"Anthropic 요청 한도 초과: 잠시 후 다시 시도하세요. ({e})") from e
        except anthropic.APIError as e:
            raise ProviderError(f"Anthropic API 오류: {e}") from e
