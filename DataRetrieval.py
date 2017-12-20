#!/usr/bin/python
# ============================================================================
# Titolo:           dataRetrieval.py
# Descrizione:      Script per estrapolare dati da un file *.txt ed inserirli in un file *.xlsx
# Autore:           Alfredo Milani (alfredo.milani.94@gmail.com)
# Data:             ven 20 ott 2017, 19.36.00, CEST
# Licenza:          MIT License
# Versione:         1.5.0
# Note:             --/--
# Versione bash:    4.4.12(1)-release
# ============================================================================
import getopt
import os
import platform
import random
import sys
from os.path import isfile

from openpyxl import Workbook
from openpyxl.worksheet.table import TableStyleInfo, Table
from pathlib import Path

import constants
import entity
from constants import APP_NAME, SystemConstants
from entity.InputData import InputData
from ui.ParseScriptUI import Colors
from utils import document_to_text
from utils.Converter import EXT_XLSX, split_char

EXIT_SUCCESS = 0
EXIT_ERR_ARG = 1
EXIT_ERR_FILE = 2
EXIT_ERR_BAD_CONTENT = 3
EXIT_ERR_PACKAGE_MISSING = 4


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
                constants.OS_WIN,
                constants.DEFAULT_TMP_WIN,
                constants.OS_LINUX,
                constants.DEFAULT_TMP_LINUX
            )
    )
    print "\t-t | --T= )\t\t\tSetting sheet title. Default behaviour: based on input filename"
    print "\t--not-ask )\t\t\tRiduces user interaction"
    print "\t--ui | --GUI )\t\t\tLaunch script in graphical mode"
    print "\t-h | -H | --help | --HELP )\tShow this help\n"


def get_program_folder():
    """
    To get absolute path of the program (path which contain the function's file)
    :rtype: str
    """
    module_file = __file__
    module_dir = os.path.split(os.path.abspath(module_file))[0]
    program_folder = os.path.abspath(module_dir)
    return program_folder


def set_up_sys():
    """
    Setup system: init global variables, loads external modules, ecc...
    :rtype: None
    """
    SystemConstants.APP_ABS_PATH = get_program_folder()
    SystemConstants.OS_TYPE = platform.system()
    if SystemConstants.OS_TYPE == constants.OS_WIN:
        SystemConstants.TMP_PATH = constants.DEFAULT_TMP_WIN
    elif SystemConstants.OS_TYPE == constants.OS_LINUX:
        SystemConstants.TMP_PATH = constants.DEFAULT_TMP_LINUX

    try:
        # import xlsxwriter;
        from openpyxl import Workbook
        from openpyxl.compat import range
        from openpyxl.utils import get_column_letter
        from openpyxl.worksheet.table import Table, TableStyleInfo
    except ImportError as err:
        print str(err)

        if SystemConstants.OS_TYPE == constants.OS_WIN:
            print "TODO: batch script to autosetup package"
            # Required with old library
            # print "Unzip file 'XlsxWriter-RELEASE_1.0.2.zip'"
            # print "Open prompt and execute 'python setup.py install'"
            # print "OR"
            # print "Try with 'pip install packagename' with admin's privileges"
            print "Perform command: 'pip install openpyxl'"
        elif SystemConstants.OS_TYPE == constants.OS_LINUX:
            print "Perform command: 'sudo pip install openpyxl'"
            # Required with old library
            # subprocess.call([INIT_SCRIPT_NAME])

        sys.exit(EXIT_ERR_PACKAGE_MISSING)


def parse_arg(argv):
    """
    Parsing list of user's input
    :type argv: list
    :rtype: InputData
    """
    input_data = InputData()

    try:
        opts, args = getopt.getopt(
            argv,
            "hHt:i:o:",
            ["not-ask", "gui", "GUI", "help", "HELP", "T=", "I=", "O=", "ifile=", "odir="]
        )
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(EXIT_ERR_ARG)

    if len(opts) == 0 and len(args) == 0:
        usage()
        sys.exit(EXIT_ERR_ARG)

    for opt, arg in opts:
        if opt in ("-h", "-H", "--help", "--HELP"):
            usage()
            sys.exit(EXIT_SUCCESS)
        elif opt in ("-i", "--I", "--ifile"):
            input_data.__setattr__("input_file", arg)
        elif opt in ("-o", "--O", "--odir"):
            input_data.__setattr__("output_dir", arg)
        elif opt in "--not-ask":
            input_data.__setattr__("verbose", False)
        elif opt in ("-t", "--T"):
            input_data.__setattr__("sheet_title", arg)
        elif opt in ("--gui", "--GUI"):
            input_data.__setattr__("gui", True)

    return input_data


def launch_ui(input_data):
    """
    Start user interface depending on user input
    :type input_data: InputData
    :rtype: None
    """
    if input_data.__getattribute__("gui"):
        import wx
        from ui import ParseScriptGUI

        graphic_interface = wx.App(False)
        SystemConstants.UI_CONSOLE = ParseScriptGUI(None, APP_NAME)
        SystemConstants.UI_CONSOLE.Show(True)
        graphic_interface.MainLoop()
    else:
        from ui.ParseScriptCLI import ParseScriptCLI

        SystemConstants.UI_CONSOLE = ParseScriptCLI()
        manage_operation(input_data)


def manage_operation(input_data):
    """
    Launch operation depending on user input
    :type input_data: InputData
    :rtype: None
    """
    input_file = input_data.__getattribute__("input_file")
    output_dir = input_data.__getattribute__("output_dir")
    sheet_title = input_data.__getattribute__("sheet_title")
    verbose = input_data.__getattribute__("verbose")

    SystemConstants.UI_CONSOLE.print_to_user("<<<--- STARTING OPERATION --->>>", Colors.TEXT_COLOR_START_OPERATION)

    if len(input_file) != 0:
        SystemConstants.UI_CONSOLE.print_to_user("Input: " + os.path.abspath(input_file))
    if len(output_dir) != 0:
        if not Path(output_dir).is_dir():
            SystemConstants.UI_CONSOLE.print_to_user(
                "Output directory '%s' not exist. Using: '%s' instead" % (output_dir, SystemConstants.TMP_PATH),
                Colors.TEXT_COLOR_WARNING
            )
            input_data.__setattr__("output_dir", SystemConstants.TMP_PATH)
            output_dir = input_data.__getattribute__("output_dir")
    else:
        input_data.__setattr__("output_dir", SystemConstants.TMP_PATH)
        output_dir = input_data.__getattribute__("output_dir")
    SystemConstants.UI_CONSOLE.print_to_user("Output directory: " + os.path.abspath(output_dir))

    if not Path(input_file).exists():
        SystemConstants.UI_CONSOLE.print_to_user("ERROR: %s not exist!" % input_file, Colors.TEXT_COLOR_ERROR)
        sys.exit(EXIT_ERR_ARG)

    if Path(input_file).is_dir():
        list_of_files = [
            input_file + split_char() + f
            for f in os.listdir(input_file)
            if isfile(input_file + split_char() + f)
        ]
    elif Path(input_file).is_file():
        list_of_files = [input_file]
    else:
        SystemConstants.UI_CONSOLE.print_to_user(
            "ERROR: %s seems not to be a regular file or directory. Exiting..." % input_file,
            Colors.TEXT_COLOR_ERROR
        )
        sys.exit(EXIT_ERR_ARG)

    SystemConstants.UI_CONSOLE.print_to_user("File that will be converted:")
    for el in list_of_files:
        SystemConstants.UI_CONSOLE.print_to_user("\t> %s" % el)

    for el in list_of_files:
        SystemConstants.UI_CONSOLE.print_to_user("\n>>> Parsing file: %s" % el)
        if verbose:
            response = SystemConstants.UI_CONSOLE.get_user_input_bool("Do you want to continue?", "Type [Yes] / [No]")

            if response:
                perform_operation(el, output_dir, sheet_title)
            else:
                SystemConstants.UI_CONSOLE.print_to_user("Skipping...")
                continue
        else:
            perform_operation(el, output_dir, sheet_title)

    SystemConstants.UI_CONSOLE.print_to_user("\n<<<--- OPERATION COMPLETED --->>>\n", Colors.TEXT_COLOR_SUCCESS)


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


def count_users(data, user_delim):
    """
    Count occurences' number of @user_delim in @data
    :type data: list
    :type user_delim: str
    :rtype: int
    """
    n = 0
    for el in data:
        if el.find(user_delim) != -1:
            n += 1

    return n


def perform_operation(input_file, output_dir="", sheet_title=""):
    """
    Perform parsing operation of file @input_file setting sheet title as @sheet_title and
    store the result in @output_dir directory
    :type input_file: str
    :type output_dir: str
    :type sheet_title: str
    :rtype: None
    """
    file_to_parse = Path(input_file)
    if not file_to_parse.is_file():
        SystemConstants.UI_CONSOLE.print_to_user("File '%s' not found" % file_to_parse, Colors.TEXT_COLOR_ERROR)
        return
        # sys.exit(EXIT_ERR_FILE)

    # conversione in base al formato del file di input
    content = document_to_text(input_file)

    if content is None:
        SystemConstants.UI_CONSOLE.print_to_user(
            "!!! Unknown format for file: %s. Skipping... !!!" % input_file,
            Colors.TEXT_COLOR_WARNING
        )
        return
        # sys.exit(EXIT_ERR_FILE)
    elif len(content) == 0:
        SystemConstants.UI_CONSOLE.print_to_user(
            "! File: %s already parsed. Skipping... !" % input_file,
            Colors.TEXT_COLOR_WARNING
        )
        return
        # sys.exit(EXIT_SUCCESS)

    # NOTE: filter returns a list in Python 2 and a generator in Python 3
    # False-ish value include: False, None, 0, '', [], () and all others empty containers
    data_list = filter(None, content.split("\n"))

    raw_data_num_users = count_users(data_list, constants.NEW_USER)

    list_of_users = get_users_list(data_list)

    if raw_data_num_users != len(list_of_users):
        SystemConstants.UI_CONSOLE.print_to_user(
            "WARNING:\tUser raw data: %d\tUser parsed: %d.\tCheck if some user missing\n" % (
                raw_data_num_users,
                len(list_of_users)
            ),
            Colors.TEXT_COLOR_WARNING
        )

    wb = Workbook()
    ws = wb.active

    # create name for new sheet
    if sheet_title is None or len(sheet_title) == 0:
        text_to_split = os.path.basename(input_file).split('.')[0]
        text_to_split = replace_unsupported_char(str(text_to_split), ['-', ' '], '_')
        month_list = text_to_split.split("_")
        try:
            if len(month_list) < 3:
                raise IndexError('Filename non in formato standard: Formsite giorno mese')
            sheet_title = month_list[len(month_list) - 2] + "-" + month_list[len(month_list) - 1][0:3]
        except IndexError:
            sheet_title = text_to_split
    ws.title = sheet_title

    # add column headings. NB. these must be strings
    ws.append(constants.HEADER_ROW)
    for user in list_of_users:
        ws.append(user.get_list_from_instance())

    # adding table to sheet
    tab = Table(displayName="Table1", ref="A1:E" + str(len(list_of_users) + 1))
    # Add a default style with striped rows and banded columns
    style = TableStyleInfo(
        name="TableStyleMedium9",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=True
    )
    tab.tableStyleInfo = style
    ws.add_table(tab)

    default_out = os.path.basename(input_file)
    default_out = os.path.splitext(default_out)[0] + EXT_XLSX
    if output_dir[len(output_dir) - 1] != '/' or output_dir[len(output_dir) - 1] != '\\':
        output_dir += split_char()
    file_to_save = output_dir + default_out

    if Path(file_to_save).exists():
        response = SystemConstants.UI_CONSOLE.get_user_input_bool(
            "File: %s already exist.\nDo you want to override it?\n" % file_to_save,
            "Type [Yes] / [No]"
        )

        if not response:
            # TODO potrebbe ancora esistere un file con lo stesso nome -> genera codice da funzione hash
            file_to_save = file_to_save[:-len(EXT_XLSX)] + "_" + str(random.randint(0, 100000)) + EXT_XLSX

    wb.save(file_to_save)
    SystemConstants.UI_CONSOLE.print_to_user("<<< File parsed >>>")


def check_match(to_match, list_to_check):
    """
    Verifica, anche parziale, del matching tra l'elemento @to_match e gli elementi di @list_to_check
    :type to_match: str
    :type list_to_check: list
    :rtype: int
    """
    for i in range(len(list_to_check)):
        if list_to_check[i] in to_match:
            return i

    return -1


def get_users_list_oldest(content):
    """
    Crea una lista di tipo User da @content
    :param content: list
    :return: list
    """
    users_list = []
    i = 0
    while i < len(content):
        # new user found
        if constants.NEW_USER in content[i]:
            name = ""
            surname = ""
            email = ""
            ntel = ""
            scores = []

            i += 1

            # parsing scores
            s = 0
            score_list = [x[0] for x in constants.SCORES_LIST]
            for score in range(constants.SCORES_NUM):
                while True:
                    item_position = check_match(content[i], score_list)
                    if item_position != -1 or constants.NEW_USER in content[i]:
                        break
                    i += 1

                if constants.NEW_USER in content[i]:
                    break

                i += 1
                if content[i] != constants.SCORE_VAL_NEGATIVE:
                    if content[i] == constants.SCORE_VAL_POSITIVE:
                        scores.append(constants.SCORES_LIST[item_position][1])
                    else:
                        SystemConstants.UI_CONSOLE.print_to_user(
                            "Error parsing value of line: %s.\tValue: %s.\tPosizione elemento della lista: %d.\n" % (
                                content[i - 1], content[i], i),
                            Colors.TEXT_COLOR_WARNING
                        )
                        continue

                i += 1
                s += 1

            # parsing credentials
            c = 0
            for credential in range(constants.CREDENTIALS_NUM):
                while True:
                    item_position = check_match(content[i], constants.CREDENTIALS_LIST)
                    if item_position != -1 or constants.NEW_USER in content[i]:
                        break
                    i += 1

                if constants.NEW_USER in content[i]:
                    break

                i += 1
                if constants.CREDENTIALS_LIST[item_position] == constants.CREDENTIAL_NAME:
                    name = content[i]
                elif constants.CREDENTIALS_LIST[item_position] == constants.CREDENTIALS_SURNAME:
                    surname = content[i]
                elif constants.CREDENTIALS_LIST[item_position] == constants.CREDENTIAL_EMAIL:
                    email = content[i]
                elif constants.CREDENTIALS_LIST[item_position] == constants.CREDENTIAL_NTEL:
                    ntel = content[i]

                i += 1
                c += 1

            user = entity.User(name, email, surname, ntel, scores)
            users_list.append(user)
            if s != constants.SCORES_NUM or c != constants.CREDENTIALS_NUM:
                SystemConstants.UI_CONSOLE.print_to_user(
                    "WARNING: Error parsing User: " + user + "\n",
                    Colors.TEXT_COLOR_WARNING
                )

            if constants.NEW_USER in content[i]:
                continue

        i += 1

    return users_list


def get_users_list_old(content):
    """
    Crea una lista di tipo User da @content
    :type content: list
    :rtype: list
    """
    score_list = [x[0] for x in constants.SCORES_LIST]
    users_list = []
    i = 0
    while i < len(content):
        # New user found
        if constants.NEW_USER in content[i]:
            name = ""
            surname = ""
            email = ""
            ntel = ""
            scores = []

            s, c = 0, 0
            while i + 1 < len(content) and constants.NEW_USER not in content[i + 1] and \
                    i + 2 < len(content) and constants.NEW_USER not in content[i + 2]:
                i += 1
                item_position = check_match(content[i], score_list)
                # Item found in scores
                if item_position != -1:
                    i += 1
                    s += 1
                    if content[i] != constants.SCORE_VAL_NEGATIVE:
                        if content[i] == constants.SCORE_VAL_POSITIVE:
                            scores.append(constants.SCORES_LIST[item_position][1])
                        else:
                            # Per far stampare anche l'utente interessato
                            s -= 1
                            SystemConstants.UI_CONSOLE.print_to_user(
                                "Error parsing value of line: %s.\tValue: %s.\tPosizione elemento della lista: %d." %
                                (content[i - 1], content[i], i),
                                Colors.TEXT_COLOR_WARNING
                            )

                    continue

                item_position = check_match(content[i], constants.CREDENTIALS_LIST)
                # Item found in credentilas
                if item_position != -1:
                    i += 1
                    c += 1
                    if constants.CREDENTIALS_LIST[item_position] == constants.CREDENTIAL_NAME:
                        name = content[i]
                    elif constants.CREDENTIALS_LIST[item_position] == constants.CREDENTIALS_SURNAME:
                        surname = content[i]
                    elif constants.CREDENTIALS_LIST[item_position] == constants.CREDENTIAL_EMAIL:
                        email = content[i]
                    elif constants.CREDENTIALS_LIST[item_position] == constants.CREDENTIAL_NTEL:
                        ntel = content[i]

            if len(name) != 0 or len(email) != 0 or len(surname) != 0 or len(ntel) != 0 or len(scores) != 0:
                user = entity.User(name, email, surname, ntel, scores)
                users_list.append(user)
                if s != constants.SCORES_NUM or c != constants.CREDENTIALS_NUM:
                    SystemConstants.UI_CONSOLE.print_to_user(
                        "WARNING: Error parsing User: " + user + " at position: " + str(i) + " / " + str(i + 1) + "\n",
                        Colors.TEXT_COLOR_WARNING
                    )

        i += 1

    return users_list


def get_users_list(content):
    """
    Crea una lista di tipo User da @content
    :type content: list
    :rtype: list
    """
    score_list = [x[0] for x in constants.SCORES_LIST]
    users_list = []
    i = 0
    while i < len(content):
        # New user found
        if constants.NEW_USER in content[i]:
            name = ""
            surname = ""
            email = ""
            ntel = ""
            scores = []

            s, c = 0, 0
            while i + 1 < len(content) and constants.NEW_USER not in content[i + 1]:
                i += 1
                item_position = check_match(content[i], score_list)
                # Item found in scores
                if item_position != -1:
                    if i + 1 >= len(content) or constants.NEW_USER in content[i + 1]:
                        break
                    elif check_match(content[i + 1], score_list) != -1 or \
                            check_match(content[i + 1], constants.CREDENTIALS_LIST) != -1:
                        SystemConstants.UI_CONSOLE.print_to_user(
                            "Unexpected parsing new value even if current is not parsed for user: " + user +
                            "\tPosizione elemento della lista: %d." % i,
                            Colors.TEXT_COLOR_WARNING
                        )
                        continue

                    i += 1
                    if content[i] != constants.SCORE_VAL_NEGATIVE:
                        if content[i] == constants.SCORE_VAL_POSITIVE:
                            scores.append(constants.SCORES_LIST[item_position][1])
                        else:
                            SystemConstants.UI_CONSOLE.print_to_user(
                                "Error parsing score value for the line: '%s'.\tValue: '%s'.\t"
                                "Posizione elemento della lista: %d." %
                                (content[i - 1], content[i], i),
                                Colors.TEXT_COLOR_WARNING
                            )
                            continue

                    s += 1
                    continue

                item_position = check_match(content[i], constants.CREDENTIALS_LIST)
                # Item found in credentials
                if item_position != -1:
                    if i + 1 >= len(content) or constants.NEW_USER in content[i + 1]:
                        break
                    elif check_match(content[i + 1], score_list) != -1 or \
                            check_match(content[i + 1], constants.CREDENTIALS_LIST) != -1:
                        SystemConstants.UI_CONSOLE.print_to_user(
                            "Unexpected parsing new value even if current is not parsed for user: " + user +
                            "\tPosizione elemento della lista: %d." % i,
                            Colors.TEXT_COLOR_WARNING
                        )
                        continue

                    i += 1
                    c += 1
                    if constants.CREDENTIALS_LIST[item_position] == constants.CREDENTIAL_NAME:
                        name = content[i]
                    elif constants.CREDENTIALS_LIST[item_position] == constants.CREDENTIALS_SURNAME:
                        surname = content[i]
                    elif constants.CREDENTIALS_LIST[item_position] == constants.CREDENTIAL_EMAIL:
                        email = content[i]
                    elif constants.CREDENTIALS_LIST[item_position] == constants.CREDENTIAL_NTEL:
                        ntel = content[i]

            if name or email or surname or ntel or scores:
                user = entity.User(name, email, surname, ntel, scores)
                users_list.append(user)
                if s != constants.SCORES_NUM or c != constants.CREDENTIALS_NUM:
                    # Check non effettuato durante l'assegnazione (nel parsing delle credenziali) dal momento che
                    # la funzione filter elimina tutti i valori Falseish, quindi i valori
                    # Checking only primary key name and email (as in https://www.prolon.it/contact-us/)
                    if not name or not email:
                        SystemConstants.UI_CONSOLE.print_to_user(
                            "Error parsing credential (name or email empty) for User: " + user,
                            Colors.TEXT_COLOR_WARNING
                        )
                    elif s == constants.SCORES_NUM:
                        continue

                    SystemConstants.UI_CONSOLE.print_to_user(
                        "WARNING: The user may have been converted incorrectly: " + user + "\n",
                        Colors.TEXT_COLOR_WARNING
                    )
            else:
                SystemConstants.UI_CONSOLE.print_to_user(
                    "WARNING: User with all empty entry at position: " + str(i) + " / " + str(i + 1) + "\n",
                    Colors.TEXT_COLOR_WARNING
                )

        i += 1

    return users_list


if __name__ == "__main__":
    set_up_sys()
    launch_ui(parse_arg(sys.argv[1:]))
    # ON WINDOWS system uncomment this line
    # launch_ui(parse_arg(["--gui"]))
