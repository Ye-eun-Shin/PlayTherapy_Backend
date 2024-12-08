class ServiceException(Exception):
    """Service Exception"""

    pass


class InvalidToken(ServiceException):
    """Invalid Token"""

    def __init__(self, token: str):
        self.message = f"access token [{token}] is invalid"
        self.status_code = 401
        self.error_code = 0
        super().__init__(self.message)


class ScriptNotFound(ServiceException):
    """Script Not found"""

    def __init__(self, session_id: int):
        self.message = f"No script found for session ID {session_id}"
        self.status_code = 400
        self.error_code = 6
        super().__init__(self.message)
