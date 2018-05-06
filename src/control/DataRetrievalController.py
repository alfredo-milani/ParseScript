import sys

from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from pathlib import Path

import constants
from constants import SystemConstants
from control.threads.ParseThread import ParseThread
from model.BaseFileFactory.BaseFileFactory import BaseFileFactory
from model.BaseFileFactory.Directory import Directory
from model.BaseFileFactory.File import File
from model import InputParams
from parsing_exceptions import FileNotFound, FileException
from utils import Common
from view import ColorsUI, DataRetrievalUI


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
            ParseThread.get_lock()
            response = self.__view_instance.get_user_input_bool(
                "File: %s already exist.\nDo you want to override it?\n" % file_to_save,
                "Type [Yes] / [No]"
            )
            ParseThread.release_lock()

            if not response:
                file_to_save = output_dir.filename + file_to_parse.get_new_basename()

        wb.save(file_to_save)

        ParseThread.get_lock()
        self._file_parsed(
            file_to_parse.filename,
            file_to_parse.conversion_algorithm.logs.get_logs()
        )
        file_to_parse.conversion_algorithm.logs.clear_logs()
        ParseThread.release_lock()

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

        self.__view_instance.print_to_user("Files that will be parsed:")
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

        threads = []
        for el in input.files:
            if verbose:
                ParseThread.get_lock()
                response = self.__view_instance.get_user_input_bool(
                    "Do you want to continue?",
                    "Type [Yes] / [No]"
                )

                if not response:
                    self.__view_instance.print_to_user("File %s skipped." % el)
                    continue
                ParseThread.release_lock()

            thread = ParseThread(
                target=self._perform_operation,
                target_args=(el, output, sheet_title)
            )
            threads.append(thread)
            thread.start()

        # if not input_data.gui:
        for thread in threads:
            thread.join()

        self.__view_instance.print_to_user(
            "\n<<<--- OPERATION COMPLETED --->>>\n",
            ColorsUI.TEXT_COLOR_SUCCESS
        )

    def _file_parsed(self, filename, logs):
        self.__view_instance.print_to_user("\n>>> Parsing file: %s" % filename)
        for el in logs:
            self.__view_instance.print_to_user(
                el[1],
                ColorsUI.get_color_from_log_type(el[0])
            )
        self.__view_instance.print_to_user("<<< File parsed >>>")
