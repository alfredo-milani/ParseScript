import sys
import thread

from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from pathlib import Path

import constants
from constants import SystemConstants
from model.BaseFileFactory.BaseFileFactory import BaseFileFactory
from model.BaseFileFactory.Directory import Directory
from model.BaseFileFactory.File import File
from parsing_exceptions import FileNotFound, FileException
from utils import *
from view import DataRetrievalUI, ColorsUI


class DataRetrievalController(object):
    """
    Controllore per le view che estendono l'interfaccia in view/DataRetrievalUI
    """

    def __init__(self):
        super(DataRetrievalController, self).__init__()
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

    def _perform_operation(self, file_to_parse, output_dir, sheet_title=""):
        """
        Perform parsing operation of file @file_to_parse setting sheet title as @sheet_title and
        store the result in @output_dir directory
        :type file_to_parse: File
        :type output_dir: Directory
        :type sheet_title: str
        :rtype: None
        """

        # In questo modo l'algoritmo, tramite la classe astratta BaseAlgorithm e ConversationAlgorithm
        # puo' accedere all'istanza di view per comunicare eventi all'utente
        # TODO vedere se conviene levare la referenza alla view mettendo una variabile che contiene
        # tutti gli errori sollevati durante l'esecuzione
        file_to_parse.conversion_algorithm.view_instance = self.__view_instance
        list_of_users = file_to_parse.get_list_from_file()

        wb = Workbook()
        ws = wb.active

        # TODO start - code to delete; eliminare codice seguente; non permettere all'utente di inserire lo sheetname
        # Create name for new sheet
        if sheet_title is None or len(sheet_title) == 0:
            text_to_split = file_to_parse.get_basename_without_exstension()
            text_to_split = Common.replace_unsupported_char(str(text_to_split), ['-', ' '], '_')
            month_list = text_to_split.split("_")
            try:
                if len(month_list) < 3:
                    raise IndexError('Filename non in formato standard: Formsite giorno mese')
                sheet_title = month_list[len(month_list) - 2] + "-" + month_list[len(month_list) - 1][0:3]
            except IndexError:
                sheet_title = text_to_split
        ws.title = sheet_title
        # TODO end - code to delete

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

        file_to_save = output_dir.filename + file_to_parse.get_parsed_basename()

        if Path(file_to_save).exists():
            response = self.__view_instance.get_user_input_bool(
                "File: %s already exist.\nDo you want to override it?\n" % file_to_save,
                "Type [Yes] / [No]"
            )

            if not response:
                file_to_save = output_dir.filename + file_to_parse.get_new_basename()

        wb.save(file_to_save)

    def manage_operation(self, input_data):
        """
        Launch operation depending on user input
        :type input_data: InputParams
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

        input = BaseFileFactory().get_file(input_file)
        if input is None:
            self.__view_instance.print_to_user(
                "ERROR: < %s > not exist or is not a regular file or link!" % input_file,
                ColorsUI.TEXT_COLOR_ERROR
            )
            self.__view_instance.print_to_user(
                "\n<<<--- OPERATION COMPLETED --->>>\n",
                ColorsUI.TEXT_COLOR_SUCCESS
            )
            sys.exit(SystemConstants.EXIT_ERR_ARG)

        try:
            output = Directory(output_dir)
        except (FileNotFound, FileException):
            self.__view_instance.print_to_user(
                "Output directory < %s > not exist or is not a directory. Using: '%s' instead" %
                (output_dir, SystemConstants.TMP_PATH),
                ColorsUI.TEXT_COLOR_WARNING
            )
            output_dir = input_data.output_dir = SystemConstants.TMP_PATH
            try:
                output = Directory(output_dir)
            except FileNotFound:
                self.__view_instance.print_to_user(
                    "Internal error: problem with temp directory < %s >." % SystemConstants.TMP_PATH,
                    ColorsUI.TEXT_COLOR_ERROR
                )
                self.__view_instance.print_to_user(
                    "\n<<<--- OPERATION COMPLETED --->>>\n",
                    ColorsUI.TEXT_COLOR_SUCCESS
                )
                sys.exit(SystemConstants.EXIT_ERR_ARG)

        self.__view_instance.print_to_user("Input: %s" % input.filename)
        self.__view_instance.print_to_user("Output directory: %s" % output.filename)

        self.__view_instance.print_to_user("File that will be parsed:")
        for el in input.files:
            self.__view_instance.print_to_user("\t> %s" % el.filename)

        if isinstance(input, Directory) and input.files_with_bad_exstension:
            self.__view_instance.print_to_user(
                "File with bad exstensione that will not be parsed:",
                ColorsUI.TEXT_COLOR_WARNING
            )

            for el in input.files_with_bad_exstension:
                self.__view_instance.print_to_user(
                    "\t> %s" % el,
                    ColorsUI.TEXT_COLOR_WARNING
                )

        for el in input.files:
            self.__view_instance.print_to_user("\n>>> Parsing file: %s" % el.filename)
            if verbose:
                response = self.__view_instance.get_user_input_bool(
                    "Do you want to continue?",
                    "Type [Yes] / [No]"
                )

                if not response:
                    self.__view_instance.print_to_user("Skipping...")
                    continue

            # thread.start_new_thread(self._perform_operation, (el, output, sheet_title))

            self._perform_operation(el, output, sheet_title)
            self.__view_instance.print_to_user("<<< File parsed >>>")

        self.__view_instance.print_to_user(
            "\n<<<--- OPERATION COMPLETED --->>>\n",
            ColorsUI.TEXT_COLOR_SUCCESS
        )
