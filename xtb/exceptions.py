

class XtbException(Exception):
    """
    Base exception for the library exceptions
    """
    pass


class XtbApiError(XtbException):
    """
    Raised if the XTB Api returns a message that contains 'status': False
    """
    def __init__(self, *args: object, code: str, description: str) -> None:
        super().__init__(*args)
        self.code = code
        self.description = description

    def __str__(self) -> str:
        return 'There was an error connecting to the API. ' \
               f'{self.code}: {self.description}'


class XtbSocketError(XtbException):
    """
    Raised for the client-side socket errors
    """
    pass
