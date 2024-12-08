class ServiceException(Exception):
    """Service Exception"""

    pass


class CaseNotFound(ServiceException):
    """Case Not found"""

    def __init__(self, case_id: int):
        self.message = f"Case {case_id} not found"
        self.status_code = 400
        self.error_code = 2
        super().__init__(self.message)


class SessionNotFound(ServiceException):
    """Session Not found"""

    def __init__(self, session_id: int):
        self.message = f"Session {session_id} not found"
        self.status_code = 400
        self.error_code = 3
        super().__init__(self.message)


class VideoNotFound(ServiceException):
    """Video Not found"""

    def __init__(self, session_id: int):
        self.message = f"No video found for session ID {session_id}"
        self.status_code = 400
        self.error_code = 5
        super().__init__(self.message)


class ScriptNotFound(ServiceException):
    """Script Not found"""

    def __init__(self, session_id: int):
        self.message = f"No script found for session ID {session_id}"
        self.status_code = 400
        self.error_code = 6
        super().__init__(self.message)


class AnalyzeReportNotFound(ServiceException):
    """Analyze Report Not found"""

    def __init__(self, session_id: int):
        self.message = f"No analyze report found for session ID {session_id}"
        self.status_code = 400
        self.error_code = 7
        super().__init__(self.message)


class InvalidRange(ServiceException):
    """Invalid Range"""

    def __init__(self, skip: int, limit: int):
        self.message = f"Invalid range {skip} to {limit}"
        self.status_code = 400
        self.error_code = 4
        super().__init__(self.message)
