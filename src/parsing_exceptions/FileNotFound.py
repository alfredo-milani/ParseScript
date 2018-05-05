class FileNotFound(Exception):
    """

    """

    def __init__(self, *args, **kwargs):
        super(FileNotFound, self).__init__(
            "Il file %s sembra non esistere o non essere un file regolare." % str(*args),
            **kwargs
        )
