import sys

from view import DataRetrievalUI


class DataRetrievalCLI(DataRetrievalUI):
    """
    CLI user interface
    """

    def __init__(self):
        super(DataRetrievalCLI, self).__init__()

    def print_to_user(self, message, message_type=DataRetrievalUI.Colors.TEXT_COLOR_DEFAULT):
        if message:
            color = DataRetrievalCLI.ColorsCLI.get_color_from_code(message_type)
            print color + message + DataRetrievalCLI.ColorsCLI.get_default_color()
            DataRetrievalCLI.__flush_stdout_buffer()

    def clear_console(self):
        print self.ColorsCLI.get_color_to_clear_console()
        '''
        This solution not delete old chars
        osname = os.name
        if osname == 'posix':
            os.system('clear')
        elif osname == 'nt' or osname == 'dos':
            os.system('cls')
        else:
            print('\n' * 30)
        '''

    def get_user_input_bool(self, question="", format_answere=""):
        print question + " " + format_answere + "\t"
        DataRetrievalCLI.__flush_stdout_buffer()

        py3 = sys.version_info[0] > 2
        if py3:
            response = str(input())
        else:
            response = str(raw_input())

        return response == "Yes"

    @staticmethod
    def __flush_stdout_buffer():
        sys.stdout.flush()

    # noinspection PyUnresolvedReferences
    class ColorsCLI(DataRetrievalUI.Colors):
        """
        Defining colors for CLI
        """

        def __init__(self):
            super(DataRetrievalCLI.ColorsCLI, self).__init__()

        @staticmethod
        def __choose_code_color_OS__(color_code):
            from constants import SystemConstants
            if SystemConstants.OS_TYPE == SystemConstants.OS_WIN:
                return ""
            else:
                if color_code == DataRetrievalUI.Colors.TEXT_COLOR_ERROR:
                    return "\033[0;31m"
                elif color_code == DataRetrievalUI.Colors.TEXT_COLOR_WARNING:
                    return "\033[1;33m"
                elif color_code == DataRetrievalUI.Colors.TEXT_COLOR_SUCCESS:
                    return "\033[0;32m"
                elif color_code == DataRetrievalUI.Colors.TEXT_COLOR_START_OPERATION:
                    return "\033[1;30m"
                elif color_code == DataRetrievalUI.Colors.TEXT_COLOR_DEFAULT:
                    return "\033[0m"

        COLOR_RED = __choose_code_color_OS__.__func__(DataRetrievalUI.Colors.TEXT_COLOR_ERROR)
        COLOR_YELLOW = __choose_code_color_OS__.__func__(DataRetrievalUI.Colors.TEXT_COLOR_WARNING)
        COLOR_GREEN = __choose_code_color_OS__.__func__(DataRetrievalUI.Colors.TEXT_COLOR_SUCCESS)
        COLOR_GRAY_DARK = __choose_code_color_OS__.__func__(DataRetrievalUI.Colors.TEXT_COLOR_START_OPERATION)
        COLOR_NONE = __choose_code_color_OS__.__func__(DataRetrievalUI.Colors.TEXT_COLOR_DEFAULT)
        STYLE_UNDERLINED = "\033[4m"
        CLEAR_CONSOLE = "\033c"

        TERMINAL_DEFAULT_COLOR = (DataRetrievalUI.Colors.TEXT_COLOR_DEFAULT, COLOR_NONE)
        TERMINAL_WARNING_COLOR = (DataRetrievalUI.Colors.TEXT_COLOR_WARNING, COLOR_YELLOW)
        TERMINAL_ERROR_COLOR = (DataRetrievalUI.Colors.TEXT_COLOR_ERROR, COLOR_RED)
        TERMINAL_SUCCESS_COLOR = (DataRetrievalUI.Colors.TEXT_COLOR_SUCCESS, COLOR_GREEN)
        TERMINAL_START_OPERATION_COLOR = (DataRetrievalUI.Colors.TEXT_COLOR_START_OPERATION, COLOR_GRAY_DARK)

        TERMINAL_COLORS = [
            TERMINAL_DEFAULT_COLOR,
            TERMINAL_ERROR_COLOR,
            TERMINAL_SUCCESS_COLOR,
            TERMINAL_START_OPERATION_COLOR,
            TERMINAL_WARNING_COLOR
        ]

        @classmethod
        def get_color_from_code(cls, type_code):
            for color in cls.TERMINAL_COLORS:
                if color[0] == type_code:
                    return color[1]

            return cls.get_default_color()

        @classmethod
        def get_default_color(cls):
            return cls.TERMINAL_DEFAULT_COLOR[1]

        @classmethod
        def get_color_to_clear_console(cls):
            return cls.CLEAR_CONSOLE
