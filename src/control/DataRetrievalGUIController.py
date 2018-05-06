import os
import subprocess
import sys

import wx

from constants import SystemConstants
from control import DataRetrievalController


class DataRetrievalGUIController(DataRetrievalController):
    """
    Controllore per le view che estendono l'interfaccia in view/build
    """

    def __init__(self):
        super(DataRetrievalGUIController, self).__init__()

    def handle_clear(self):
        if self.view_instance.user_console:
            self.view_instance.user_console.SetValue("")

    def handle_start(self):
        input_file = self.view_instance.edittextfile.GetValue()
        input_dir = self.view_instance.edittextdirinput.GetValue()
        output_dir = self.view_instance.edittextdiroutput.GetValue()
        verbose = self.view_instance.checkboxverbose.GetValue()

        # CHECK INPUT
        from pathlib import Path
        if len(input_file) == 0 or not Path(str(input_file)).exists():
            input_file = None

        if len(input_dir) == 0 or not Path(str(input_dir)).exists():
            input_dir = None

        # se esistono entrambi i path (input file e input directory), considero solo il path che punta ad una directory
        if input_dir is not None:
            input_file = input_dir

        if input_file is None and input_dir is None:
            self.__alert_on_error("Error loading file: check if the input file exist!", "Wrong path")
            return

        # CHECK OUTPUT
        if len(output_dir) == 0 or not Path(str(output_dir)).exists():
            self.__alert_on_error("Error: check if the output location exist!", "Wrong path")
            return

        # START OPERATION
        from model import InputParams
        input_data = InputParams(input_file, output_dir, verbose=verbose, gui=True)
        # TODO rendere GUI risponsiva -> fare chiamata che non blocchi il MainLoop della GUI
        super(DataRetrievalGUIController, self).manage_operation(input_data)

    def handle_show_files(self, url):
        self.__open_file(url)

    def handle_quit(self):
        self.view_instance.Close()

    @staticmethod
    def handle_help():
        dial = wx.MessageDialog(
            None,
            SystemConstants.HELP_MSG,
            "Help",
            wx.OK | wx.ICON_QUESTION
        )
        dial.ShowModal()

    @staticmethod
    def handle_filename_selected(edittext, message):
        path = wx.FileSelector(
            message=message,
            wildcard="File (*.txt,*.pdf,*.docx,*.xlsx)|*.txt;*.pdf;*.docx;*.xlsx",
            default_path=SystemConstants.APP_ABS_PATH
        )

        if path is not None:
            edittext.SetValue(path)

    @staticmethod
    def handle_directory_selected(edittext, message):
        path = wx.DirSelector(
            message=message,
            default_path=SystemConstants.APP_ABS_PATH
        )

        if path is not None:
            edittext.SetValue(path)

    @staticmethod
    def __alert_on_error(message, windows_name):
        dial = wx.MessageDialog(None, message, windows_name, wx.OK | wx.ICON_ERROR)
        dial.ShowModal()

    @staticmethod
    def __open_file(outputdirectory):
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
