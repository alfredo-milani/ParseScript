from abc import abstractmethod


class ParseScriptUI(object):
    """
    Interface to interact with user
    """

    @abstractmethod
    def print_to_user(self, message="", message_type=0):
        """
        Show @message to user of color @message_type: default (0), green (1), red (-1), grey (2)
        :param message: string
        :param message_type: int
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def get_user_input(self, question="", format_answere=""):
        """
        Get input from user depending on @question message with @format_answere as options
        :param question: string
        :param format_answere: string
        :return: bool
        """
        raise NotImplementedError
