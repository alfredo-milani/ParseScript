from abc import abstractmethod


class BaseFile(object):
    """

    """

    def __init__(self):
        super(BaseFile, self).__init__()

    @property
    @abstractmethod
    def files(self):
        """

        :return:
        :rtype: list
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def is_dir(self):
        """

        :return:
        :rtype: bool
        """
        raise NotImplementedError
