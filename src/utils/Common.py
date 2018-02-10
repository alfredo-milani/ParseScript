# coding=utf-8
import getopt
import os
import platform
import sys

from constants import SystemConstants


class Common(object):

    @staticmethod
    def get_program_folder():
        """
        To get absolute path of the program (path which contain current function's file)
        So this function return the path previous to utils/ProjectPath directory
        :rtype: str
        """
        from utils import Converter
        module_file = __file__
        module_dir = os.path.split(os.path.abspath(module_file))[0]
        program_folder = os.path.abspath(module_dir)
        program_folder_list = program_folder.split(Converter.split_char())
        root_project = Converter.split_char().join(
            x for x in program_folder_list[:len(program_folder_list) - 1]
        )
        return root_project

    @staticmethod
    def usage():
        """
        Show usage to user on CLI
        :return: None
        """
        print SystemConstants.USAGE_MSG

    @staticmethod
    def set_up_sys():
        """
        Setup system: init global variables, loads external modules, ecc...
        :rtype: None
        """
        from utils import Converter
        SystemConstants.APP_ABS_PATH = Common.get_program_folder()
        SystemConstants.APP_ABS_RES = SystemConstants.APP_ABS_PATH + Converter.split_char() + \
                                      ".." + Converter.split_char() + "resources" + Converter.split_char()
        SystemConstants.OS_TYPE = platform.system()
        # Windows system
        if SystemConstants.OS_TYPE == SystemConstants.OS_WIN:
            SystemConstants.TMP_PATH = SystemConstants.DEFAULT_TMP_WIN
        # Unix system
        elif SystemConstants.OS_TYPE == SystemConstants.OS_LINUX:
            SystemConstants.TMP_PATH = SystemConstants.DEFAULT_TMP_LINUX

    @staticmethod
    def parse_arg(argv):
        """
        Parsing list of user's input
        :type argv: list
        :rtype: InputData
        """
        try:
            opts, args = getopt.getopt(
                argv,
                "hHt:i:o:",
                ["not-ask", "gui", "GUI", "help", "HELP", "T=", "I=", "O=", "ifile=", "odir="]
            )
        except getopt.GetoptError as err:
            print str(err)
            Common.usage()
            sys.exit(SystemConstants.EXIT_ERR_ARG)

        if len(opts) == 0 and len(args) == 0:
            Common.usage()
            sys.exit(SystemConstants.EXIT_ERR_ARG)

        input_file = ""
        output_dir = ""
        sheet_title = ""
        verbose = True
        gui = False
        for opt, arg in opts:
            if opt in ("-h", "-H", "--help", "--HELP"):
                Common.usage()
                sys.exit(SystemConstants.EXIT_SUCCESS)
            elif opt in ("-i", "--I", "--ifile"):
                input_file = arg
            elif opt in ("-o", "--O", "--odir"):
                output_dir = arg
            elif opt in "--not-ask":
                verbose = False
            elif opt in ("-t", "--T"):
                sheet_title = arg
            elif opt in ("--gui", "--GUI"):
                gui = True

        from model import InputData
        return InputData(input_file, output_dir, sheet_title, verbose, gui)

    @staticmethod
    def replace_unsupported_char(string, chars_to_check, selected_char):
        """
        Replace @chars_to_check with @selected_char in @string
        :type string: str
        :type chars_to_check: list
        :type selected_char: str
        :rtype: str
        """
        for char in chars_to_check:
            string = string.replace(char, selected_char)

        return string
