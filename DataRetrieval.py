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

from openpyxl import Workbook
from openpyxl.worksheet.table import TableStyleInfo, Table
from pathlib import Path

import GetFileDialog
import constants
import entity
from support import document_to_text
from support.Converter import EXT_TXT, EXT_XLSX

EXIT_SUCCESS = 0
EXIT_ERR_ARG = 1
EXIT_ERR_FILE = 2
EXIT_ERR_BAD_CONTENT = 3
EXIT_ERR_PACKAGE_MISSING = 4

FILE_SPLIT_CHAR = '/'


def usage():
    print "\n# Utilizzo\n"
    print "\t./" + os.path.basename(__file__) + " [Options]\n"
    print "# Options\n"
    print "\t-i | --I= | --ifile= )\t\tSetting input file"
    print (
        "\t-o | --O= | --ofile= )\t\tSetting output file. If not specified, a file (*%s) "
        "will be created in the default temp directory ('%s' -> '%s' | '%s' -> '%s')" % (
            EXT_XLSX,
            constants.OS_WIN,
            constants.DEFAULT_TMP_WIN,
            constants.OS_LINUX,
            constants.DEFAULT_TMP_LINUX
        )
    )
    print "\t-t | --T= )\t\t\tSetting sheet title. Default behaviour: based on input filename"
    print "\t--auto-convert )\tAutoconvert file *docx insted of using file *.txt"
    print "\t--gui | --GUI )\tLaunch script in graphical mode"
    print "\t-h | -H | --help | --HELP )\tShow this help\n"


def set_up_sys():
    try:
        # import xlsxwriter;
        from openpyxl import Workbook
        from openpyxl.compat import range
        from openpyxl.utils import get_column_letter
        from openpyxl.worksheet.table import Table, TableStyleInfo
    except ImportError as err:
        print str(err)

        os_type = platform.system()
        if os_type == constants.OS_WIN:
            print "TODO: batch script to autosetup package"
            # Required with old library
            # print "Unzip file 'XlsxWriter-RELEASE_1.0.2.zip'"
            # print "Open prompt and execute 'python setup.py install'"
            # print "OR"
            # print "Try with 'pip install packagename' with admin's privileges"
            print "Perform command: 'pip install openpyxl'"
        elif os_type == constants.OS_LINUX:
            print "Perform command: 'sudo pip install openpyxl'"
            # Required with old library
            # subprocess.call([INIT_SCRIPT_NAME])

        sys.exit(EXIT_ERR_PACKAGE_MISSING)


def parse_arg(argv):
    input_file = ""
    output_file = ""
    sheet_title = ""

    try:
        opts, args = getopt.getopt(
            argv,
            "hHt:i:o:",
            ["auto-convert", "gui", "GUI", "help", "HELP", "T=", "I=", "O=", "ifile=", "ofile="]
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
            input_file = arg
        elif opt in ("-o", "--O", "--ofile"):
            output_file = arg
        elif opt in ("-t", "--T"):
            sheet_title = arg
        elif opt in ("--gui", "--GUI"):
            gui_laucher()

    print "\nNOTA: Probabilmente a causa di un problema di codifica/decodicifa, i files che mi hai " \
          "dato direttamente in formato *.txt non vengono eleaborati. Per elaborare i dati io ho " \
          "aperto un file in formato *.docx e ho utilizzato la funzione 'salva con nome' e ho " \
          "salvato il file in formato 'Testo (.txt)' (senza codifica)\n"

    print (
        "NOTA: su %s --> utilizza il link '%s' per convertire il file *docx in *txt. "
        "Una volta convertito esegui il comando: "
        "'python X:\script_dir\script.py --I Y:\\file_to_parse.txt --O Z:\create_new_file.xlsx'\n" %
        (constants.OS_WIN, constants.LINK_TOOL_CONVERTER_DOCX_TXT)
    )

    print "Current directory: ", os.getcwd()

    if len(input_file) != 0:
        print "Input file: ", os.path.abspath(input_file)
    if len(output_file) != 0:
        print "Output file: ", os.path.abspath(output_file)
    continue_str = "Do you want to continue? Type [Yes] / [No]\n"
    py3 = sys.version_info[0] > 2
    if py3:
        response = input(continue_str)
    else:
        response = raw_input(continue_str)

    if response == "Yes":
        perform_operation(input_file, output_file, sheet_title)
    else:
        print "Exiting..."
        sys.exit(EXIT_SUCCESS)


def gui_laucher():
    GetFileDialog.laucher()


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


def perform_operation(input_file, output_file="", sheet_title=""):
    file_to_parse = Path(input_file)
    if not file_to_parse.is_file():
        print ("File '%s' not found" % file_to_parse)
        sys.exit(EXIT_ERR_FILE)

    # conversione in base al formato del file di input
    filename_list = input_file.rsplit(FILE_SPLIT_CHAR, 1)
    filename = filename_list[len(filename_list) - 1]
    if filename[-4:] == EXT_TXT:
        with open(input_file, "r") as file_to_parse:
            content = file_to_parse.read()
    else:
        content = document_to_text(input_file)

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

    file_to_save = output_file
    default_out = os.path.basename(input_file)
    default_out = os.path.splitext(default_out)[0] + EXT_XLSX
    if len(file_to_save) != 0:
        if EXT_XLSX not in file_to_save:
            file_to_save += EXT_XLSX
    else:
        os_type = platform.system()
        if os_type == constants.OS_WIN:
            file_to_save = constants.DEFAULT_TMP_WIN
        elif os_type == constants.OS_LINUX:
            file_to_save = constants.DEFAULT_TMP_LINUX
        file_to_save += default_out

    if Path(file_to_save).exists():
        user_cmd = "File: %s already exist. Do you want to override it? [Yes / No]\n" % file_to_save
        py3 = sys.version_info[0] > 2
        if py3:
            response = input(user_cmd)
        else:
            response = raw_input(user_cmd)
        if response != "Yes":
            file_to_save = file_to_save.split(".")[0] + str(random.randint(0, 100000)) + EXT_XLSX

    wb.save(file_to_save)


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
                            "Error parsing value of line: %s.\nValue: %s.\nLine: %d." % (
                                content[i - 1],
                                content[i],
                                i
                            )
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
    parse_arg(sys.argv[1:])
