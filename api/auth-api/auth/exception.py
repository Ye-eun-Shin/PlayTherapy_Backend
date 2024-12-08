class ServiceException(Exception):
    """Service Exception"""

    pass


class UserAlreadyExist(ServiceException):
    """User Already Exist"""

    def __init__(self, email: str):
        self.message = f"User email [{email}] already exist"
        self.status_code = 400
        self.error_code = 1
        super().__init__(self.message)


class UserNotFound(ServiceException):
    """User Not Found"""

    def __init__(self, email: str):
        self.message = (
            f"There is no information matching the user's email [{email}] and password."
        )
        self.status_code = 404
        self.error_code = 0
        super().__init__(self.message)


class InvalidUserEmail(ServiceException):
    """Invalid User Email"""

    def __init__(self, email: str):
        self.message = f"User email [{email}] is invalid"
        self.status_code = 400
        self.error_code = 0
        super().__init__(self.message)
