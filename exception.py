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


class SyntaxError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class TokenizeError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
