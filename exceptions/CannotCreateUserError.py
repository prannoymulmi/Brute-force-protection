class CannotCreateUserError(Exception):
    """ Exception raised when staff is not found in the database.

    Attributes:
        message -- explanation of the error

    """

    def __init__(self, message: str = "Cannot create User") -> None:
        self.message = message
        super().__init__(self.message)

