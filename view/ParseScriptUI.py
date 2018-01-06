from abc import abstractmethod


class ParseScriptUI(object):
    """
    Contract to interact with user
    """

    class Colors(object):
        """
        Contract which define color of user interface
        """

        TEXT_COLOR_DEFAULT = 0
        TEXT_COLOR_WARNING = -2
        TEXT_COLOR_ERROR = -1
        TEXT_COLOR_SUCCESS = 1
        TEXT_COLOR_START_OPERATION = 2

        @staticmethod
        @abstractmethod
        def get_color_from_code(type_code):
            """
            Get correct color from @color_list based on @type_code.
            In case of errors return @Color (data type based on selected UI)
            :type type_code: int
            :rtype: Any
            """
            raise NotImplementedError

        @staticmethod
        @abstractmethod
        def get_default_color():
            """
            Get default color
            :rtype: Any
            """
            raise NotImplementedError

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
