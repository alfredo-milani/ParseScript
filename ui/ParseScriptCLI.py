import sys

from ui.ParseScriptUI import ParseScriptUI, Colors


class ColorsCLI(Colors):
    COLOR_RED = "\033[0;31m"
    COLOR_YELLOW = "\033[1;33m"
    COLOR_GREEN = "\033[0;32m"
    COLOR_GRAY_DARK = "\033[1;30m"
    COLOR_NONE = "\033[0m"
    STYLE_UNDERLINED = "\033[4m"
    CLEAR_CONSOLE = "\033c"

    TERMINAL_DEFAULT_COLOR = (Colors.TEXT_COLOR_DEFAULT, COLOR_NONE)
    TERMINAL_WARNING_COLOR = (Colors.TEXT_COLOR_WARNING, COLOR_YELLOW)
    TERMINAL_ERROR_COLOR = (Colors.TEXT_COLOR_ERROR, COLOR_RED)
    TERMINAL_SUCCESS_COLOR = (Colors.TEXT_COLOR_SUCCESS, COLOR_GREEN)
    TERMINAL_START_OPERATION_COLOR = (Colors.TEXT_COLOR_START_OPERATION, COLOR_GRAY_DARK)

    TERMINAL_COLORS = [
        TERMINAL_DEFAULT_COLOR,
        TERMINAL_ERROR_COLOR,
        TERMINAL_SUCCESS_COLOR,
        TERMINAL_START_OPERATION_COLOR,
        TERMINAL_WARNING_COLOR
    ]


class ParseScriptCLI(ParseScriptUI):
    def print_to_user(self, message="", message_type=ColorsCLI.TEXT_COLOR_DEFAULT):
        if message is not None:
            color = ColorsCLI.get_color_from_code(
                message_type,
                ColorsCLI.TERMINAL_COLORS,
                ColorsCLI.TERMINAL_DEFAULT_COLOR[1]
            )
            print color + message + ColorsCLI.TERMINAL_DEFAULT_COLOR[1]
            self.__flush_stdout_buffer__()

    def clear_console(self):
        print ColorsCLI.CLEAR_CONSOLE
        '''
        Solution less "strong"
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
        self.__flush_stdout_buffer__()

        py3 = sys.version_info[0] > 2
        if py3:
            response = str(input())
        else:
            response = str(raw_input())

        return response == "Yes"

    @staticmethod
    def __flush_stdout_buffer__():
        sys.stdout.flush()
