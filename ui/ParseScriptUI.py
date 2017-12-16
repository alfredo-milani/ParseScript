from abc import abstractmethod


class Colors(object):
    """
    Class containing colors
    """

    TEXT_COLOR_DEFAULT = 0
    TEXT_COLOR_WARNING = -2
    TEXT_COLOR_ERROR = -1
    TEXT_COLOR_SUCCESS = 1
    TEXT_COLOR_START_OPERATION = 2

    @staticmethod
    def get_color_from_code(type_code, color_list, default_color):
        """
        Get correct color from @color_list based on @type_code.
        In case of errors return @Color (data type based on selected UI)
        :type type_code: int
        :type color_list: list
        :type default_color: Any
        :rtype: Any
        """
        for color in color_list:
            if color[0] == type_code:
                return color[1]

        return default_color


class ParseScriptUI(object):
    """
    Interface to interact with user
    """

    @abstractmethod
    def print_to_user(self, message="", message_type=Colors.TEXT_COLOR_DEFAULT):
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
