class LLMServiceError(Exception):
    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = 503,
    ) -> None:
        super().__init__(message)

        self.message = message
        self.error_code = error_code
        self.status_code = status_code


class AgentServiceError(Exception):
    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = 500,
    ) -> None:
        super().__init__(message)

        self.message = message
        self.error_code = error_code
        self.status_code = status_code