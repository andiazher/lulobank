from exceptions import messages


class ApiException(Exception):

    def __init__(self, type, status, code, value_to_format=None):
        self.type = type
        self.status = status
        self.code = code
        self.message = messages.get_message(code, value_to_format)


class ClientException(ApiException):
    pass


class LambdaException(ApiException):
    pass
