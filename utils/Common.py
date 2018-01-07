import getopt
import os
import platform
import sys

from constants import SystemConstants
from model import InputData
from utils import Converter


def get_program_folder():
    """
    To get absolute path of the program (path which contain current function's file)
    So this function return the path previous to utils/ProjectPath directory
    :rtype: str
    """
    module_file = __file__
    module_dir = os.path.split(os.path.abspath(module_file))[0]
    program_folder = os.path.abspath(module_dir)
    program_folder_list = program_folder.split(Converter.split_char())
    root_project = Converter.split_char().join(
        x for x in program_folder_list[:len(program_folder_list) - 1]
    )
    return root_project


def usage():
    """
    Show usage to user on CLI
    :return: None
    """
    print "\n# Utilizzo\n"
    print "\t./" + os.path.basename(__file__) + " [Options]\n"
    print "# Options\n"
    print "\t-i | --I= | --ifile= )\t\tSetting input file"
    print (
            "\t-o | --O= | --odir= )\t\tSetting output directory. If not specified the files "
            "will be created in the default temp directory ('%s' -> '%s' | '%s' -> '%s')" % (
                SystemConstants.OS_WIN,
                SystemConstants.DEFAULT_TMP_WIN,
                SystemConstants.OS_LINUX,
                SystemConstants.DEFAULT_TMP_LINUX
            )
    )
    print "\t-t | --T= )\t\t\tSetting sheet title. Default behaviour: based on input filename"
    print "\t--not-ask )\t\t\tRiduces user interaction"
    print "\t--view | --GUI )\t\t\tLaunch script in graphical mode"
    print "\t-h | -H | --help | --HELP )\tShow this help\n"


def set_up_sys():
    """
    Setup system: init global variables, loads external modules, ecc...
    :rtype: None
    """
    SystemConstants.APP_ABS_PATH = get_program_folder()
    SystemConstants.OS_TYPE = platform.system()
    # Windows system
    if SystemConstants.OS_TYPE == SystemConstants.OS_WIN:
        SystemConstants.TMP_PATH = SystemConstants.DEFAULT_TMP_WIN
    # Unix system
    elif SystemConstants.OS_TYPE == SystemConstants.OS_LINUX:
        SystemConstants.TMP_PATH = SystemConstants.DEFAULT_TMP_LINUX


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
        usage()
        sys.exit(SystemConstants.EXIT_ERR_ARG)

    if len(opts) == 0 and len(args) == 0:
        usage()
        sys.exit(SystemConstants.EXIT_ERR_ARG)

    input_file = ""
    output_dir = ""
    sheet_title = ""
    verbose = True
    gui = False
    for opt, arg in opts:
        if opt in ("-h", "-H", "--help", "--HELP"):
            usage()
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

    return InputData(input_file, output_dir, sheet_title, verbose, gui)
