class SingletonException(Exception):
    """

    """

    def __init__(self, *args, **kwargs):
        super(SingletonException, self).__init__(
            "Non puo' essere creata piu' di una istanza della classe %s" % str(*args),
            **kwargs
        )
