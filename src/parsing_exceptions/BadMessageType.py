class BadMessageType(Exception):
    """

    """

    def __init__(self, *args, **kwargs):
        super(BadMessageType, self).__init__(
            "Tipo di messaggio non supportato: %s" % str(*args),
            **kwargs
        )
