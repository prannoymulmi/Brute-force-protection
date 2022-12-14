class UserNotFoundError(Exception):
    """ Exception raised when staff is not found in the database.

    Attributes:
        message -- explanation of the error

    """

    def __init__(self, message: str = "Staff is not Found") -> None:
        self.message = message
        super().__init__(self.message)

