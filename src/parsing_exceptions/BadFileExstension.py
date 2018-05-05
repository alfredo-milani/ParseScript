class BadFileExstension(Exception):
    """

    """

    def __init__(self, *args, **kwargs):
        super(BadFileExstension, self).__init__(
            "Il file %s ha una estensione non supportata." % str(*args),
            **kwargs
        )
