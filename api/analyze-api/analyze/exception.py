class ServiceException(Exception):
    """Service Exception"""

    pass


class ObservationNotFound(ServiceException):
    def __init__(self, prompt_id: int):
        self.message = f"Observation {prompt_id} not found"
        self.status_code = 400
        self.error_code = 100
        super().__init__(self.message)
