class LLMClient:
    def summarize(self, text: str) -> str:
        return text[:300]
