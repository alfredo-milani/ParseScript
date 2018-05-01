from abc import abstractmethod

from view import DataRetrievalUI


class ConversationAlgorithm(object):
    """
    Classe astratta utilizzata per gestire l'esecuzione dell'algoritmo di parsing
    """

    EXT_XLSX = ".xlsx"
    EXT_TXT = ".txt"
    EXT_DOC = ".doc"
    EXT_DOCX = ".docx"
    EXT_ODT = ".odt"
    EXT_PDF = ".pdf"

    ENCODE_UTF_8 = "utf-8"
    DECODE_FORMAT = "utf-8"

    def __init__(self):
        self.list_of_users = None
        # View reference
        self.__view_instance = None

    @property
    def view_instance(self):
        return self.__view_instance

    @view_instance.setter
    def view_instance(self, value):
        if not isinstance(value, DataRetrievalUI):
            raise TypeError("Incorrect instance")

        self.__view_instance = value

    @property
    def list_of_users(self):
        return self.__list_of_users

    @list_of_users.setter
    def list_of_users(self, value):
        # PyCharm inspection bug
        self.__list_of_users = value

    def convertToList(self, file_to_convert):
        """
        DO NOT EDIT this function!
        This function define conversation algorithm.
        :type file_to_convert: str
        :rtype: list
        """
        self.do_before_convert()
        self.list_of_users = self.do_convert(file_to_convert)
        self.do_after_convert()

        return self.list_of_users

    def do_before_convert(self):
        """
        Actions to perform before that conversion algorithm is triggered
        :rtype: None
        """
        pass

    @abstractmethod
    def do_convert(self, file_to_convert):
        """
        Algoritmo per convertire @file_to_convert in una lista di @User
        :param file_to_convert: file from which parse users
        :type file_to_convert: str

        :return: list of users parsed from @file_to_convert
        :rtype: list
        """
        raise NotImplementedError

    def do_after_convert(self):
        """
        Actions to perform after that conversion algorithm is triggered
        :rtype: None
        """
        pass
