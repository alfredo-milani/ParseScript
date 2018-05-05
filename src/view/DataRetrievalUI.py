from abc import abstractmethod

from view import ColorsUI


class DataRetrievalUI(object):
    """
    Contract to interact with user
    """

    def __init__(self):
        super(DataRetrievalUI, self).__init__()

    @abstractmethod
    def print_to_user(self, message, message_type=ColorsUI.TEXT_COLOR_DEFAULT):
        """
        Show @message to user of color @message_type: default (0), green (1), red (-1), grey (2)
        :type message: str
        :type message_type: int
        :rtype: None
        """
        raise NotImplementedError

    @abstractmethod
    def clear_console(self):
        """
        Clean console output
        :rtype: None
        """
        raise NotImplementedError

    @abstractmethod
    def get_user_input_bool(self, question="", format_answere=""):
        """
        Get input from user depending on @question message with @format_answere as options
        :type format_answere: str
        :type question: str
        :rtype: bool
        """
        raise NotImplementedError
