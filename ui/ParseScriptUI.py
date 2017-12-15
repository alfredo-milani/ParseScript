from abc import abstractmethod

TEXT_COLOR_DEFAULT = 0
TEXT_COLOR_WARNING = -2
TEXT_COLOR_ERROR = -1
TEXT_COLOR_SUCCESS = 1
TEXT_COLOR_START_OPERATION = 2


class ParseScriptUI(object):
    """
    Interface to interact with user
    """

    @staticmethod
    def get_color_from_code(type_code, color_list, default_color):
        """
        Get correct color from @color_list based on @type_code.
        In case of errors return @Color (data type based on selected UI)
        :param type_code: int
        :param color_list: list
        :param default_color: Color
        :return: Color
        """
        for color in color_list:
            if color[0] == type_code:
                return color[1]

        return default_color

    @abstractmethod
    def print_to_user(self, message="", message_type=TEXT_COLOR_DEFAULT):
        """
        Show @message to user of color @message_type: default (0), green (1), red (-1), grey (2)
        :param message: string
        :param message_type: int
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def clear_console(self):
        """
        Clean console output
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
