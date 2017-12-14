import sys

from ui.ParseScriptUI import ParseScriptUI

TEXT_COLOR_DEFAULT = 0
TEXT_COLOR_WARNING = -2
TEXT_COLOR_ERROR = -1
TEXT_COLOR_SUCCESS = 1
TEXT_COLOR_START_OPERATION = 2


class ParseScriptCLI(ParseScriptUI):
    def print_to_user(self, message="", message_type=0):
        if message is not None:
            print message
            self.__flush_stdout_buffer__()

    def get_user_input(self, question="", format_answere=""):
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
