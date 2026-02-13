from .services.runtime import RuntimeService

runtime_service = RuntimeService()


def get_runtime() -> RuntimeService:
    return runtime_service
