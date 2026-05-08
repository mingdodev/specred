from openai import OpenAI, APIError, AuthenticationError, RateLimitError

from specred.providers.base import LLMProvider, ProviderError


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str) -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def complete(self, system: str, user: str) -> str:
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                max_tokens=4096,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            return response.choices[0].message.content
        except AuthenticationError as e:
            raise ProviderError(f"OpenAI 인증 실패: API 키를 확인하세요. ({e})") from e
        except RateLimitError as e:
            raise ProviderError(f"OpenAI 요청 한도 초과: 잠시 후 다시 시도하세요. ({e})") from e
        except APIError as e:
            raise ProviderError(f"OpenAI API 오류: {e}") from e
