class FileException(Exception):
    """

    """

    def __init__(self, *args, **kwargs):
        super(FileException, self).__init__(
            *args,
            **kwargs
        )
