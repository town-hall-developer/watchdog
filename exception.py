class DateTimeFormatException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidDatasourceException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidFunctionException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class SyntaxException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class TokenizeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
