class Logging(object):
    """

    """

    E = "Error"
    W = "Warning"
    N = "Normal"
    S = "Special"

    __message_type = [E, W, N, S]

    def __init__(self):
        super(Logging, self).__init__()
        self.__logs = []

    def get_logs(self):
        return self.__logs

    def append_logs(self, message_type, value):
        found = False
        for t in Logging.__message_type:
            if t == message_type:
                found = True
        if not found:
            from parsing_exceptions import BadMessageType
            raise BadMessageType(message_type)

        self.__logs.append((str(message_type), str(value)))

    def clear_logs(self):
        del self.__logs[:]
