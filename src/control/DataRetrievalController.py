import os
import random
import sys
from os.path import isfile

from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from pathlib import Path

import constants
from constants import SystemConstants
from model import *
from utils import *
from view import DataRetrievalUI, ColorsUI
from control.convertStrategy import ConversationAlgorithm


class DataRetrievalController(object):
    """
    Controllore per le view che estendono l'interfaccia in view/DataRetrievalUI
    """

    def __init__(self):
        # View reference
        self.__view_instance = None

    @property
    def view_instance(self):
        return self.__view_instance

    @view_instance.setter
    def view_instance(self, value):
        if not isinstance(value, DataRetrievalUI):
            raise TypeError("Incorrect instance")

        self.__view_instance = value

    def __perform_operation(self, input_file, output_dir, sheet_title=""):
        """
        Perform parsing operation of file @input_file setting sheet title as @sheet_title and
        store the result in @output_dir directory
        :type input_file: str
        :type output_dir: str
        :type sheet_title: str
        :rtype: None
        """

        try:
            file_to_parse = File(input_file)
        except IOError:
            self.__view_instance.print_to_user(
                "File '%s' not found\nSkipping..." % input_file,
                ColorsUI.TEXT_COLOR_ERROR
            )
            return
            # sys.exit(EXIT_ERR_FILE)
        except TypeError:
            self.__view_instance.print_to_user(
                "File '%s' has bad extension\nSkipping..." % input_file,
                ColorsUI.TEXT_COLOR_ERROR
            )
            return
            # sys.exit(EXIT_ERR_FILE)

        # In questo modo l'algoritmo, tramite la classe astratta BaseAlgorithm e ConversationAlgorithm
        # puo' accedere all'istanza di view per comunicare eventi all'utente
        file_to_parse.conversion_algorithm.view_instance = self.__view_instance
        try:
            list_of_users = file_to_parse.get_list_from_file()
        except IOError:
            list_of_users = None

        wb = Workbook()
        ws = wb.active

        # Create name for new sheet
        if sheet_title is None or len(sheet_title) == 0:
            text_to_split = os.path.basename(input_file).split('.')[0]
            text_to_split = Common.replace_unsupported_char(str(text_to_split), ['-', ' '], '_')
            month_list = text_to_split.split("_")
            try:
                if len(month_list) < 3:
                    raise IndexError('Filename non in formato standard: Formsite giorno mese')
                sheet_title = month_list[len(month_list) - 2] + "-" + month_list[len(month_list) - 1][0:3]
            except IndexError:
                sheet_title = text_to_split
        ws.title = sheet_title

        # Add column headings. NB. these must be strings
        ws.append(constants.HEADER_ROW)
        for user in list_of_users:
            ws.append(user.get_list_from_instance())

        # Adding table to sheet
        tab = Table(displayName="Data", ref="A1:J" + str(len(list_of_users) + 1))
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
        default_out = os.path.splitext(default_out)[0] + ConversationAlgorithm.EXT_XLSX
        if output_dir[len(output_dir) - 1] != '/' and output_dir[len(output_dir) - 1] != '\\':
            output_dir += Common.split_char()
        file_to_save = output_dir + default_out

        if Path(file_to_save).exists():
            response = self.__view_instance.get_user_input_bool(
                "File: %s already exist.\nDo you want to override it?\n" % file_to_save,
                "Type [Yes] / [No]"
            )

            if not response:
                # TODO potrebbe ancora esistere un file con lo stesso nome -> genera codice da funzione hash
                file_to_save = file_to_save[:-len(ConversationAlgorithm.EXT_XLSX)] + "_" + \
                               str(random.randint(0, 100000)) + ConversationAlgorithm.EXT_XLSX

        wb.save(file_to_save)
        self.__view_instance.print_to_user("<<< File parsed >>>")

    def _manage_operation(self, input_data):
        """
        Launch operation depending on user input
        :type input_data: InputData
        :rtype: None
        """
        input_file = input_data.input_file
        output_dir = input_data.output_dir
        sheet_title = input_data.sheet_title
        verbose = input_data.verbose

        self.__view_instance.print_to_user(
            "<<<--- STARTING OPERATION --->>>",
            ColorsUI.TEXT_COLOR_START_OPERATION
        )

        if len(input_file) != 0:
            self.__view_instance.print_to_user("Input: " + os.path.abspath(input_file))
        if len(output_dir) != 0:
            if not Path(output_dir).is_dir():
                self.__view_instance.print_to_user(
                    "Output directory '%s' not exist. Using: '%s' instead" % (output_dir, SystemConstants.TMP_PATH),
                    ColorsUI.TEXT_COLOR_WARNING
                )
                input_data.output_dir = SystemConstants.TMP_PATH
                output_dir = input_data.output_dir
        else:
            input_data.output_dir = SystemConstants.TMP_PATH
            output_dir = input_data.output_dir
        self.__view_instance.print_to_user("Output directory: " + os.path.abspath(output_dir))

        if not Path(input_file).exists():
            self.__view_instance.print_to_user(
                "ERROR: %s not exist!" % input_file,
                ColorsUI.TEXT_COLOR_ERROR
            )
            sys.exit(SystemConstants.EXIT_ERR_ARG)

        if Path(input_file).is_dir():
            list_of_files = [
                input_file + Common.split_char() + f
                for f in os.listdir(input_file)
                if isfile(input_file + Common.split_char() + f)
            ]
        elif Path(input_file).is_file():
            list_of_files = [input_file]
        else:
            self.__view_instance.print_to_user(
                "ERROR: %s seems not to be a regular file or directory. Exiting..." % input_file,
                ColorsUI.TEXT_COLOR_ERROR
            )
            sys.exit(SystemConstants.EXIT_ERR_ARG)

        self.__view_instance.print_to_user("File that will be converted:")
        for el in list_of_files:
            self.__view_instance.print_to_user("\t> %s" % el)

        for el in list_of_files:
            self.__view_instance.print_to_user("\n>>> Parsing file: %s" % el)
            if verbose:
                response = self.__view_instance.get_user_input_bool(
                    "Do you want to continue?",
                    "Type [Yes] / [No]"
                )

                if not response:
                    self.__view_instance.print_to_user("Skipping...")
                    continue

            self.__perform_operation(el, output_dir, sheet_title)

        self.__view_instance.print_to_user(
            "\n<<<--- OPERATION COMPLETED --->>>\n",
            ColorsUI.TEXT_COLOR_SUCCESS
        )
