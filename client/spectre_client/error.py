class ProtocolError(Exception):

    def __init__(self, request, error, message):
        self.request = request
        self.error = error
        self.message = message

    def __str__(self):
        return 'ProtocolError: {} on request "{}"'.format(self.error, self.request)

class ConnectionClosedError(Exception):
	pass