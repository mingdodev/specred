from google import genai
from google.genai import types
from google.api_core.exceptions import GoogleAPICallError, PermissionDenied, ResourceExhausted, Unauthenticated

from specred.providers.base import LLMProvider, ProviderError


class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str, model: str) -> None:
        self._client = genai.Client(api_key=api_key)
        self._model = model

    def complete(self, system: str, user: str) -> str:
        try:
            response = self._client.models.generate_content(
                model=self._model,
                contents=user,
                config=types.GenerateContentConfig(
                    system_instruction=system,
                    max_output_tokens=4096,
                ),
            )
            return response.text
        except (Unauthenticated, PermissionDenied) as e:
            raise ProviderError(f"Gemini 인증 실패: API 키를 확인하세요. ({e})") from e
        except ResourceExhausted as e:
            raise ProviderError(f"Gemini 할당량 초과: 플랜/결제 정보를 확인하거나 잠시 후 다시 시도하세요. ({e})") from e
        except GoogleAPICallError as e:
            raise ProviderError(f"Gemini API 오류: {e}") from e
