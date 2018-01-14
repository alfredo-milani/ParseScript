import os
import subprocess
import sys

import wx
from pathlib import Path

from constants import SystemConstants
from model.InputData import InputData
from utils import split_char
from view.ParseScriptUI import ParseScriptUI


class ParseScriptGUI(wx.Frame, ParseScriptUI):
    """
    GUI user interface
    """

    APP_EXIT = 1
    APP_HELP_HINT = 2
    APP_START = 3
    APP_SELECT_INPUT_FILE = 4
    APP_SELECT_OUTPUT_DIR = 5
    APP_SELECT_INPUT_DIR = 6
    APP_SHOW_PARSED_FILES = 8
    APP_CLEAN_CONSOLE = 7

    def __init__(self, parent, title):
        super(ParseScriptGUI, self).__init__(parent, id=wx.ID_ANY, title=title, pos=wx.DefaultPosition, size=(900, 500))

        # Objects that will be used
        self.user_console = None
        self.edittextfile = None
        self.edittextdirinput = None
        self.edittextdiroutput = None
        self.checkboxverbose = None
        ###
        self.init_view()
        self.Centre()

    def init_view(self):
        # CREATE PANEL
        panel = wx.Panel(self)

        # SET ICON
        # ON PACKAGING remove "SystemConstants.APP_ABS_PATH + split_char() + " from the following icon's path.
        # ON PACKAGING on Windows system the icon must be in *.ico format;
        # after pyinstaller is executed move the executable in the root of the project.
        icon = wx.Icon(
            SystemConstants.APP_ABS_PATH + split_char() +
            "resources" + split_char() +
            "images" + split_char() + "icon.png",
            wx.BITMAP_TYPE_PNG,
            512,
            512
        )
        self.SetIcon(icon)

        # MENU ITEMS
        menubar = wx.MenuBar()

        filemenu = wx.Menu()
        quitmenuitem = wx.MenuItem(filemenu, ParseScriptGUI.APP_EXIT, '&Quit\tCtrl+Q')
        '''
        # ON WINDOWS viene mostrata non ridimensionata
        # ON UNIX systems (Debian) non viene mostrata
        quitmenuitem.SetBitmap(wx.Bitmap(os.path.join(
            SystemConstants.APP_ABS_PATH,
            "resources" + split_char() + "images" + split_char() + "exit.png"
        )))
        '''

        helpmenu = wx.Menu()
        helpmenuitem = wx.MenuItem(helpmenu, ParseScriptGUI.APP_HELP_HINT, "&Help\tCtrl+H")

        filemenu.Append(quitmenuitem)
        helpmenu.Append(helpmenuitem)

        menubar.Append(filemenu, '&File')
        menubar.Append(helpmenu, "&Help")
        self.SetMenuBar(menubar)

        # FONT
        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(12)

        # BOX SIZER
        mainbox = wx.BoxSizer(wx.VERTICAL)

        # INPUT BOX
        inputbox = wx.BoxSizer(wx.HORIZONTAL)

        inputstatictext = wx.StaticText(panel, label='Select input file or directory')
        inputstatictext.SetFont(font)

        inputboxpath = wx.BoxSizer(wx.VERTICAL)

        inputboxpathfileinput = wx.BoxSizer(wx.HORIZONTAL)
        self.edittextfile = wx.TextCtrl(panel)
        buttonfileinput = wx.Button(panel, label="...", size=(50, 10), id=ParseScriptGUI.APP_SELECT_INPUT_FILE)
        inputboxpathfileinput.Add(self.edittextfile, flag=wx.RIGHT, border=10, proportion=1)
        inputboxpathfileinput.Add(buttonfileinput, flag=wx.EXPAND)

        inputstatictextchoose = wx.StaticText(panel, label="OR")
        inputstatictextchoose.SetFont(font)

        inputboxpathdirinput = wx.BoxSizer(wx.HORIZONTAL)
        self.edittextdirinput = wx.TextCtrl(panel)
        buttondirinput = wx.Button(panel, label="...", size=(50, 10), id=ParseScriptGUI.APP_SELECT_INPUT_DIR)
        inputboxpathdirinput.Add(self.edittextdirinput, flag=wx.RIGHT, border=10, proportion=1)
        inputboxpathdirinput.Add(buttondirinput, flag=wx.EXPAND)

        inputboxpath.Add(inputboxpathfileinput, flag=wx.EXPAND)
        inputboxpath.Add(inputstatictextchoose, flag=wx.CENTER)
        inputboxpath.Add(inputboxpathdirinput, flag=wx.EXPAND)

        inputbox.Add(inputstatictext, flag=wx.RIGHT, border=10)
        inputbox.Add(inputboxpath, proportion=1)

        mainbox.Add(inputbox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # LINE SEPARATOR
        line = wx.StaticLine(panel, style=wx.HORIZONTAL)
        mainbox.Add(line, 0, wx.ALL | wx.EXPAND, 10)
        # Per aggiungere spazio
        # mainbox.Add((-1, 10))

        # OUTPUT BOX
        outputbox = wx.BoxSizer(wx.HORIZONTAL)

        outputstatictext = wx.StaticText(panel, label='Select output directory')
        outputstatictext.SetFont(font)
        self.edittextdiroutput = wx.TextCtrl(panel)
        buttondiroutput = wx.Button(panel, label="...", size=(50, 10), id=ParseScriptGUI.APP_SELECT_OUTPUT_DIR)

        outputbox.Add(outputstatictext, flag=wx.RIGHT, border=10)
        outputbox.Add(self.edittextdiroutput, flag=wx.RIGHT, border=10, proportion=1)
        outputbox.Add(buttondiroutput, flag=wx.EXPAND)

        mainbox.Add(outputbox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # LINE SEPARATOR
        line = wx.StaticLine(panel, style=wx.HORIZONTAL)
        mainbox.Add(line, 0, wx.ALL | wx.EXPAND, 10)
        # mainbox.Add((-1, 10))

        # START / STOP BUTTONS
        manageoperationbox = wx.BoxSizer(wx.HORIZONTAL)

        buttonstart = wx.Button(panel, label='Start', size=(150, 30), id=ParseScriptGUI.APP_START)
        buttonstart.SetFont(font)
        buttonclose = wx.Button(panel, label='Close', size=(150, 30), id=ParseScriptGUI.APP_EXIT)
        buttonclose.SetFont(font)

        manageoperationbox.Add(buttonstart)
        manageoperationbox.Add(buttonclose, flag=wx.LEFT | wx.BOTTOM, border=5)

        mainbox.Add(manageoperationbox, flag=wx.CENTER, border=30)

        # LINE SEPARATOR
        line = wx.StaticLine(panel, style=wx.HORIZONTAL)
        mainbox.Add(line, 0, wx.ALL | wx.EXPAND, 10)
        # mainbox.Add((-1, 10))

        # LOG TOOLS
        logbox = wx.BoxSizer(wx.HORIZONTAL)

        buttoncleanconsole = wx.Button(panel, label="Clear", id=ParseScriptGUI.APP_CLEAN_CONSOLE, size=(50, 30))
        buttoncleanconsole.SetFont(font)
        buttonshowfiles = wx.Button(panel, label="Files", id=ParseScriptGUI.APP_SHOW_PARSED_FILES, size=(50, 30))
        buttonshowfiles.SetFont(font)
        self.checkboxverbose = wx.CheckBox(panel, label="Verbose")
        self.checkboxverbose.SetFont(font)
        statictextlogs = wx.StaticText(panel, label='Logs')
        font.SetPointSize(12)
        statictextlogs.SetFont(font)

        logbox.Add(buttoncleanconsole, flag=wx.ALIGN_CENTER_VERTICAL)
        logbox.Add(buttonshowfiles, flag=wx.ALIGN_CENTER_VERTICAL)
        logbox.Add(self.checkboxverbose, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL)
        logbox.Add(statictextlogs, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL)

        mainbox.Add(logbox, border=10, flag=wx.ALL | wx.EXPAND)

        # LOG CONSOLE
        consolebox = wx.BoxSizer(wx.HORIZONTAL)

        edittextconsole = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        edittextconsole.SetEditable(False)
        font.SetPointSize(15)
        edittextconsole.SetFont(font)
        # Change background console color on Windows systems
        if SystemConstants.OS_TYPE == SystemConstants.OS_WIN:
            edittextconsole.SetBackgroundColour((148, 162, 183))

        global USER_CONSOLE
        USER_CONSOLE = edittextconsole
        self.user_console = edittextconsole

        consolebox.Add(edittextconsole, proportion=1, flag=wx.EXPAND | wx.BOTTOM, border=5)

        mainbox.Add(
            consolebox,
            proportion=1,
            flag=wx.LEFT | wx.RIGHT | wx.EXPAND,
            border=5
        )

        # SET BOX TO THE PANEL
        panel.SetSizer(mainbox)

        # BINDINGS WIDGETS
        self.Bind(wx.EVT_MENU, self.on_quit, id=ParseScriptGUI.APP_EXIT)
        self.Bind(wx.EVT_MENU, self.on_help, id=ParseScriptGUI.APP_HELP_HINT)
        self.Bind(wx.EVT_BUTTON, self.on_quit, id=ParseScriptGUI.APP_EXIT)
        self.Bind(wx.EVT_BUTTON, self.on_show_parsed_files, id=ParseScriptGUI.APP_SHOW_PARSED_FILES)
        self.Bind(
            wx.EVT_BUTTON,
            lambda event: self.clear_console(),
            # button e id si possono anche usare in mutua esclusione
            # buttoncleanconsole,
            id=ParseScriptGUI.APP_CLEAN_CONSOLE
        )
        self.Bind(
            wx.EVT_BUTTON,
            lambda event: self.on_start(),
            id=ParseScriptGUI.APP_START
        )
        self.Bind(
            wx.EVT_BUTTON,
            lambda event: self.on_show_parsed_files(self.edittextdiroutput.GetValue()),
            id=ParseScriptGUI.APP_SHOW_PARSED_FILES
        )
        self.Bind(
            wx.EVT_BUTTON,
            lambda event: self.on_selected_filename(self.edittextfile),
            id=ParseScriptGUI.APP_SELECT_INPUT_FILE
        )
        self.Bind(
            wx.EVT_BUTTON,
            lambda event: self.on_selected_directory(self.edittextdiroutput),
            id=ParseScriptGUI.APP_SELECT_OUTPUT_DIR
        )
        self.Bind(
            wx.EVT_BUTTON,
            lambda event: self.on_selected_directory(self.edittextdirinput),
            id=ParseScriptGUI.APP_SELECT_INPUT_DIR
        )

    @staticmethod
    def on_help(event):
        event.Skip()
        dial = wx.MessageDialog(None, SystemConstants.HELP_MSG, 'Help', wx.OK | wx.ICON_QUESTION)
        dial.ShowModal()

    def on_quit(self, event):
        event.Skip()
        self.Close()

    def on_start(self):
        input_file = self.edittextfile.GetValue()
        input_dir = self.edittextdirinput.GetValue()
        output_dir = self.edittextdiroutput.GetValue()
        verbose = self.checkboxverbose.GetValue()

        # CHECK INPUT
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
        from control import DataRetrievalController
        input_data = InputData(input_file, output_dir, verbose=verbose, gui=True)
        DataRetrievalController().manage_operation(input_data)

    @staticmethod
    def alert_on_error(message, windows_name):
        dial = wx.MessageDialog(None, message, windows_name, wx.OK | wx.ICON_ERROR)
        dial.ShowModal()

    @staticmethod
    def on_selected_filename(edittextfilename):
        path = wx.FileSelector(
            message="Select file or directory to parse",
            wildcard="File (*.txt,*.pdf,*.docx,*.xlsx)|*.txt;*.pdf;*.docx;*.xlsx",
            default_path=SystemConstants.APP_ABS_PATH
        )
        if path is not None:
            edittextfilename.SetValue(path)

    @staticmethod
    def on_selected_directory(edittextdirectory):
        path = wx.DirSelector(
            message="Select output directory",
            default_path=SystemConstants.APP_ABS_PATH
        )

        if path is not None:
            edittextdirectory.SetValue(path)

    def on_show_parsed_files(self, outputdirectory):
        self.open_file(outputdirectory)

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

    def clear_console(self):
        if self.user_console:
            self.user_console.SetValue("")

    def print_to_user(self, message, message_type=ParseScriptUI.Colors.TEXT_COLOR_DEFAULT):
        if self.user_console and message:
            self.user_console.SetForegroundColour(ParseScriptGUI.ColorsGUI.get_color_from_code(message_type))
            self.user_console.AppendText(message + "\n")
            self.user_console.SetForegroundColour(ParseScriptGUI.ColorsGUI.get_default_color())

    def get_user_input_bool(self, question="", format_answere=""):
        dlg = wx.MessageDialog(None, question, style=wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal() == wx.ID_YES
        dlg.Destroy()
        return result

    class ColorsGUI(ParseScriptUI.Colors):
        """
        Defining colors for GUI
        """

        CONSOLE_DEFAULT_COLOR = (ParseScriptUI.Colors.TEXT_COLOR_DEFAULT, wx.WHITE)
        CONSOLE_WARNING_COLOR = (ParseScriptUI.Colors.TEXT_COLOR_WARNING, wx.YELLOW)
        CONSOLE_ERROR_COLOR = (ParseScriptUI.Colors.TEXT_COLOR_ERROR, wx.RED)
        CONSOLE_SUCCESS_COLOR = (ParseScriptUI.Colors.TEXT_COLOR_SUCCESS, wx.GREEN)
        CONSOLE_START_OPERATION_COLOR = (ParseScriptUI.Colors.TEXT_COLOR_START_OPERATION, wx.CYAN)

        CONSOLE_COLORS = [
            CONSOLE_DEFAULT_COLOR,
            CONSOLE_ERROR_COLOR,
            CONSOLE_SUCCESS_COLOR,
            CONSOLE_START_OPERATION_COLOR,
            CONSOLE_WARNING_COLOR
        ]

        @staticmethod
        def get_color_from_code(type_code):
            for color in ParseScriptGUI.ColorsGUI.CONSOLE_COLORS:
                if color[0] == type_code:
                    return color[1]

            return ParseScriptGUI.ColorsGUI.get_default_color()

        @staticmethod
        def get_default_color():
            return ParseScriptGUI.ColorsGUI.CONSOLE_DEFAULT_COLOR[1]
