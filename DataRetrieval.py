#!/usr/bin/python
# ============================================================================
# Titolo:           dataRetrieval.py
# Descrizione:      Script per estrapolare dati da un file *.txt ed inserirli in un file *.xlsx
# Autore:           Alfredo Milani (alfredo.milani.94@gmail.com)
# Data:             ven 20 ott 2017, 19.36.00, CEST
# Licenza:          MIT License
# Versione:         0.7.0
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
from entity.InputData import InputData
from utils import document_to_text
from utils.Converter import EXT_XLSX, split_char

EXIT_SUCCESS = 0
EXIT_ERR_ARG = 1
EXIT_ERR_FILE = 2
EXIT_ERR_BAD_CONTENT = 3
EXIT_ERR_PACKAGE_MISSING = 4

OS_TYPE = ""
TMP_PATH = ""


def usage():
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
    print "\t--gui | --GUI )\t\t\tLaunch script in graphical mode"
    print "\t-h | -H | --help | --HELP )\tShow this help\n"


def set_up_sys():
    global OS_TYPE, TMP_PATH
    OS_TYPE = platform.system()
    if OS_TYPE == constants.OS_WIN:
        TMP_PATH = constants.DEFAULT_TMP_WIN
    elif OS_TYPE == constants.OS_LINUX:
        TMP_PATH = constants.DEFAULT_TMP_LINUX

    try:
        # import xlsxwriter;
        from openpyxl import Workbook
        from openpyxl.compat import range
        from openpyxl.utils import get_column_letter
        from openpyxl.worksheet.table import Table, TableStyleInfo
    except ImportError as err:
        print str(err)

        if OS_TYPE == constants.OS_WIN:
            print "TODO: batch script to autosetup package"
            # Required with old library
            # print "Unzip file 'XlsxWriter-RELEASE_1.0.2.zip'"
            # print "Open prompt and execute 'python setup.py install'"
            # print "OR"
            # print "Try with 'pip install packagename' with admin's privileges"
            print "Perform command: 'pip install openpyxl'"
        elif OS_TYPE == constants.OS_LINUX:
            print "Perform command: 'sudo pip install openpyxl'"
            # Required with old library
            # subprocess.call([INIT_SCRIPT_NAME])

        sys.exit(EXIT_ERR_PACKAGE_MISSING)


def parse_arg(argv):
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
            input_data.__setattr__("reduce_ask", True)
        elif opt in ("-t", "--T"):
            input_data.__setattr__("sheet_title", arg)
        elif opt in ("--gui", "--GUI"):
            input_data.__setattr__("reduce_ask", True)
            input_data.__setattr__("gui", True)

    # print "Current directory: ", os.getcwd()

    return input_data


def choose_ui(input_data):
    if input_data.__getattribute__("gui"):
        from gui import GraphicUserInterface
        GraphicUserInterface.init()
    else:
        start_operation(input_data)


def start_operation(input_data):
    input_file = input_data.__getattribute__("input_file")
    output_dir = input_data.__getattribute__("output_dir")
    sheet_title = input_data.__getattribute__("sheet_title")
    reduce_ask = input_data.__getattribute__("reduce_ask")

    if len(input_file) != 0:
        print "Input: ", os.path.abspath(input_file)
    if len(output_dir) != 0:
        if not Path(output_dir).is_dir():
            print "Output directory '%s' not exist. Using: '%s' instead" % (output_dir, TMP_PATH)
            input_data.__setattr__("output_dir", TMP_PATH)
            output_dir = input_data.__getattribute__("output_dir")
    else:
        input_data.__setattr__("output_dir", TMP_PATH)
        output_dir = input_data.__getattribute__("output_dir")
    print "Output directory: ", os.path.abspath(output_dir)
    # TODO al posto di controllare l'attributo 'gui' creare 2 classi (CLI, GUI) ed usa il polimorfismo
    sys.stdout.flush()

    if not Path(input_file).exists():
        print "ERROR: %s not exist!" % input_file
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
        print "ERROR: %s seems not to be a regular file or directory. Exiting..." % input_file
        sys.exit(EXIT_ERR_ARG)

    print "File that will be converted:"
    for el in list_of_files:
        print "\t> %s" % el
    print "\n"
    sys.stdout.flush()

    for el in list_of_files:
        print "\n\n>>> Parsing file: %s" % el
        if not reduce_ask:
            print "Do you want to continue? Type [Yes] / [No]\t"
            sys.stdout.flush()

            py3 = sys.version_info[0] > 2
            if py3:
                response = input()
            else:
                response = raw_input()

            if response == "Yes":
                perform_operation(el, output_dir, sheet_title)
            else:
                print "Skipping..."
                sys.stdout.flush()
                continue
        else:
            perform_operation(el, output_dir, sheet_title)


def replace_unsupported_char(string, chars_to_check, selected_char):
    for char in chars_to_check:
        string = string.replace(char, selected_char)

    return string


def count_users(data, user_delim):
    n = 0
    for el in data:
        if el.find(user_delim) != -1:
            n += 1

    return n


def perform_operation(input_file, output_dir="", sheet_title=""):
    file_to_parse = Path(input_file)
    if not file_to_parse.is_file():
        print ("File '%s' not found" % file_to_parse)
        return
        # sys.exit(EXIT_ERR_FILE)

    # conversione in base al formato del file di input
    content = document_to_text(input_file)

    if content is None:
        print "!!! Unknown format for file: %s. Skipping... !!!" % input_file
        sys.stdout.flush()
        return
        # sys.exit(EXIT_ERR_FILE)
    elif len(content) == 0:
        print "! File: %s already parsed. Skipping... !" % input_file
        sys.stdout.flush()
        return
        # sys.exit(EXIT_SUCCESS)

    # NOTE: filter returns a list in Python 2 and a generator in Python 3
    # False-ish value include: False, None, 0, '', [], () and all others empty containers
    data_list = filter(None, content.split("\n"))

    raw_data_num_users = count_users(data_list, constants.NEW_USER)

    list_of_users = get_users_list(data_list)

    if raw_data_num_users != len(list_of_users):
        print "WARNING:\nUser raw data: %d\nUser parsed: %d\nCheck if some user missing" % (
            raw_data_num_users,
            len(list_of_users)
        )

    wb = Workbook()
    ws = wb.active

    # create name for new sheet
    if len(sheet_title) == 0:
        text_to_split = os.path.splitext(input_file)[0]
        text_to_split = replace_unsupported_char(text_to_split, ['-', ' '], '_')
        month_list = text_to_split.split("_")
        sheet_title = month_list[1] + "-" + month_list[2][0:3]
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
        print "File: %s already exist. Do you want to override it? [Yes / No]\n" % file_to_save
        sys.stdout.flush()
        py3 = sys.version_info[0] > 2
        if py3:
            response = input()
        else:
            response = raw_input()

        if response != "Yes":
            # TODO potrebbe ancora esistere un file con lo stesso nome -> genera codice da funzione hash
            file_to_save = file_to_save[:-len(EXT_XLSX)] + "_" + str(random.randint(0, 100000)) + EXT_XLSX

    wb.save(file_to_save)
    print "<<< File correctly parsed >>>"


def get_users_list(content):
    users_list = []
    i = 0
    while i < len(content):
        # new user found
        if content[i].find(constants.NEW_USER) != -1:
            name = ""
            surname = ""
            email = ""
            ntel = ""
            scores = []

            i += 1

            # parsing scores
            s = 0
            for itemScore in constants.SCORES_LIST:
                while content[i].find(itemScore[0]) == -1 and content[i].find(constants.NEW_USER) == -1:
                    i += 1
                if content[i].find(constants.NEW_USER) != -1:
                    break

                i += 1
                if content[i] != constants.SCORE_VAL_NEGATIVE:
                    if content[i] == constants.SCORE_VAL_POSITIVE:
                        scores.append(itemScore[1])
                    else:
                        print (
                            "Error parsing value of line: %s.\nValue: %s.\nLine: %d." %
                            (content[i - 1], content[i], i)
                        )
                        continue

                s += 1

            if content[i].find(constants.NEW_USER) != -1:
                continue

            # parsing credentials
            c = 0
            for itemCredential in constants.CREDENTIALS_LIST:
                while content[i].find(itemCredential) == -1 and content[i].find(constants.NEW_USER) == -1:
                    i += 1
                if content[i].find(constants.NEW_USER) != -1:
                    break

                i += 1
                if itemCredential == constants.CREDENTIAL_NAME:
                    name = content[i]
                elif itemCredential == constants.CREDENTIALS_SURNAME:
                    surname = content[i]
                elif itemCredential == constants.CREDENTIAL_EMAIL:
                    email = content[i]
                elif itemCredential == constants.CREDENTIAL_NTEL:
                    ntel = content[i]

                c += 1

            if content[i].find(constants.NEW_USER) != -1:
                continue

            user = entity.User(name, surname, email, ntel, scores)
            users_list.append(user)
            if s != constants.SCORES_NUM or c != constants.CREDENTIALS_NUM:
                print "Warning: Wrong parsed: User: " + user

        i += 1

    return users_list


if __name__ == "__main__":
    set_up_sys()
    choose_ui(parse_arg(sys.argv[1:]))
