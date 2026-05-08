from specred.providers.base import LLMProvider

SUPPORTED_PROVIDERS = ("anthropic", "gemini", "openai")


def create_provider(provider: str, api_key: str, model: str) -> LLMProvider:
    """config의 provider/api_key/model을 받아 LLMProvider 인스턴스를 반환한다."""
    if provider == "anthropic":
        from specred.providers.anthropic import AnthropicProvider
        return AnthropicProvider(api_key=api_key, model=model)

    if provider == "gemini":
        from specred.providers.gemini import GeminiProvider
        return GeminiProvider(api_key=api_key, model=model)

    if provider == "openai":
        from specred.providers.openai import OpenAIProvider
        return OpenAIProvider(api_key=api_key, model=model)

    raise ValueError(
        f"지원하지 않는 provider: '{provider}'. "
        f"사용 가능한 provider: {', '.join(SUPPORTED_PROVIDERS)}"
    )
