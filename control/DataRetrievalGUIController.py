import os
import subprocess
import sys

import wx

from control import DataRetrievalController
from view import DataRetrievalGUI


class DataRetrievalGUIController(DataRetrievalController):
    """
    Controllore per le view che estendono l'interfaccia in view/DataRetrievalGUI
    """

    def __init__(self):
        super(DataRetrievalGUIController, self).__init__()
        # View reference
        self.__view_instance = None

    @property
    def view_instance(self):
        return self.__view_instance

    @view_instance.setter
    def view_instance(self, value):
        if not isinstance(value, DataRetrievalGUI):
            raise TypeError("Incorrect instance")

        # PyCharm inspection bug
        self.__view_instance = value

    def handle_clear(self):
        if self.__view_instance.user_console:
            self.__view_instance.user_console.SetValue("")

    def handle_start(self):
        input_file = self.__view_instance.edittextfile.GetValue()
        input_dir = self.__view_instance.edittextdirinput.GetValue()
        output_dir = self.__view_instance.edittextdiroutput.GetValue()
        verbose = self.__view_instance.checkboxverbose.GetValue()

        # CHECK INPUT
        from pathlib import Path
        if input_file is None or len(input_file) == 0 or not Path(input_file).exists():
            input_file = None

        if input_dir is None or len(input_dir) == 0 or not Path(input_dir).exists():
            input_dir = None

        if input_file is None and input_dir is None:
            self.alert_on_error("Error loading file: check if the input file exist!", "Wrong path")
            return

        # se esistono entrambi i path (input file e input directory), considero solo il path che punta ad una directory
        if input_dir is not None:
            input_file = input_dir

        # CHECK OUTPUT
        if output_dir is None or len(output_dir) == 0 or not Path(output_dir).exists():
            output_dir = None

        if output_dir is None:
            self.alert_on_error("Error: check if the output location exist!", "Wrong path")
            return

        # START OPERATION
        from model import InputData
        input_data = InputData(input_file, output_dir, verbose=verbose, gui=True)
        self.manage_operation(input_data)

    def handle_show_files(self, url):
        self.open_file(url)

    def handle_quit(self):
        self.__view_instance.Close()

    @staticmethod
    def handle_help():
        from constants import SystemConstants
        dial = wx.MessageDialog(
            None,
            SystemConstants.HELP_MSG,
            'Help',
            wx.OK | wx.ICON_QUESTION
        )
        dial.ShowModal()

    @staticmethod
    def alert_on_error(message, windows_name):
        dial = wx.MessageDialog(None, message, windows_name, wx.OK | wx.ICON_ERROR)
        dial.ShowModal()

    @staticmethod
    def open_file(outputdirectory):
        """
        Open file manager with root @filename for the correct OS
        :type outputdirectory: str
        :rtype: None
        """
        if sys.platform == "win32":
            os.startfile(outputdirectory)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, outputdirectory])
