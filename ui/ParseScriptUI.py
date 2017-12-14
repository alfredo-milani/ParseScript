from abc import abstractmethod


class ParseScriptUI(object):
    """
    Interface to interact with user
    """

    @abstractmethod
    def print_to_user(self, message=""):
        """
        Show message to user
        :param message: message to show
        """
        raise NotImplementedError

    @abstractmethod
    def get_user_input(self, question="", format_answere=""):
        """
        Get input from user
        :return: string
        """
        raise NotImplementedError
