import sys

from ui.ParseScriptUI import ParseScriptUI


class ParseScriptCLI(ParseScriptUI):
    def print_to_user(self, message=""):
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
