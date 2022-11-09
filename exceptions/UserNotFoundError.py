class UserNotFoundError(Exception):
    """ Exception raised when user is not found in the database.

    Attributes:
        message -- explanation of the error

    """

    def __init__(self, message: str = "User is not Found") -> None:
        self.message = message
        super().__init__(self.message)

