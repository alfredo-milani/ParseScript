# coding=utf-8
import os

import wx
# constants to bind functions
from pathlib import Path

from DataRetrieval import init_operation
from constants import SystemConstants
from entity.InputData import InputData
from ui.ParseScriptUI import ParseScriptUI
from utils import split_char

APP_EXIT = 1
APP_HELP_HINT = 2
APP_START = 3
APP_SELECT_INPUT_FILE = 4
APP_SELECT_OUTPUT_DIR = 5
APP_SELECT_INPUT_DIR = 6
APP_CLEAN_CONSOLE = 7

HELP_MSG = "Con questo tool è possibile fare il parsing di file in formato: *.pdf, *.txt o *.docx.\n" \
           "Si può scegliere di parsare un solo file o di parsare i files" \
           "contenuti in una specifica directory utilizzando i box appositi."

USER_CONSOLE = None


class ParseScriptGUI(wx.Frame, ParseScriptUI):
    def __init__(self, parent, title):
        super(ParseScriptGUI, self).__init__(parent, id=wx.ID_ANY, title=title, pos=wx.DefaultPosition, size=(900, 500))

        self.InitGUI()
        self.Centre()

    def InitGUI(self):
        panel = wx.Panel(self)

        # SET ICON
        icon = wx.Icon("resources" + split_char() + "images" + split_char() + "icon.png", wx.BITMAP_TYPE_PNG, 512, 512)
        self.SetIcon(icon)

        # MENU ITEMS
        menubar = wx.MenuBar()
        filemenu = wx.Menu()
        qmi = wx.MenuItem(filemenu, APP_EXIT, '&Quit\tCtrl+Q')
        qmi.SetBitmap(wx.Bitmap(os.path.join(
            SystemConstants.APP_ABS_PATH,
            "resources" + split_char() + "images" + split_char() + "exit.png"
        )))

        helpmenu = wx.Menu()
        helpmenuitem = wx.MenuItem(helpmenu, APP_HELP_HINT, "&Help\tCtrl+H")

        filemenu.Append(qmi)
        helpmenu.Append(helpmenuitem)

        menubar.Append(filemenu, '&File')
        menubar.Append(helpmenu, "&Help")
        self.SetMenuBar(menubar)

        # FONT
        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(12)

        # BOX SIZER
        vbox = wx.BoxSizer(wx.VERTICAL)

        # INPUT BOX
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label='Select input file or directory')
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.RIGHT, border=10)

        vbox1_1 = wx.BoxSizer(wx.VERTICAL)
        hbox1_1 = wx.BoxSizer(wx.HORIZONTAL)
        edittextfilein = wx.TextCtrl(panel)
        hbox1_1.Add(edittextfilein, flag=wx.RIGHT, border=10, proportion=1)
        selectfileinbutton = wx.Button(panel, label="...", size=(50, 10), id=APP_SELECT_INPUT_FILE)
        hbox1_1.Add(selectfileinbutton, flag=wx.EXPAND)
        vbox1_1.Add(hbox1_1, flag=wx.EXPAND)

        st4 = wx.StaticText(panel, label="OR")
        st4.SetFont(font)
        vbox1_1.Add(st4, flag=wx.CENTER)

        hbox1_2 = wx.BoxSizer(wx.HORIZONTAL)
        edittextdirin = wx.TextCtrl(panel)
        hbox1_2.Add(edittextdirin, flag=wx.RIGHT, border=10, proportion=1)
        selectdirinbutton = wx.Button(panel, label="...", size=(50, 10), id=APP_SELECT_INPUT_DIR)
        hbox1_2.Add(selectdirinbutton, flag=wx.EXPAND)
        vbox1_1.Add(hbox1_2, flag=wx.EXPAND)

        hbox1.Add(vbox1_1, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # LINE SEPARATOR
        line = wx.StaticLine(panel, style=wx.HORIZONTAL)
        vbox.Add(line, 0, wx.ALL | wx.EXPAND, 10)
        # vbox.Add((-1, 10))

        # OUTPUT BOX
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st3 = wx.StaticText(panel, label='Select output directory')
        st3.SetFont(font)

        hbox2.Add(st3, flag=wx.RIGHT, border=10)
        edittextdirout = wx.TextCtrl(panel)
        hbox2.Add(edittextdirout, flag=wx.RIGHT, border=10, proportion=1)
        selectdiroutbutton = wx.Button(panel, label="...", size=(50, 10), id=APP_SELECT_OUTPUT_DIR)
        hbox2.Add(selectdiroutbutton, flag=wx.EXPAND)

        vbox.Add(hbox2, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # LINE SEPARATOR
        line = wx.StaticLine(panel, style=wx.HORIZONTAL)
        vbox.Add(line, 0, wx.ALL | wx.EXPAND, 10)
        # vbox.Add((-1, 10))

        # START / STOP BUTTONS
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='Start', size=(150, 30), id=APP_START)
        hbox3.Add(btn1)
        btn2 = wx.Button(panel, label='Close', size=(150, 30), id=APP_EXIT)
        hbox3.Add(btn2, flag=wx.LEFT | wx.BOTTOM, border=5)
        vbox.Add(hbox3, flag=wx.CENTER, border=30)

        # LINE SEPARATOR
        line = wx.StaticLine(panel, style=wx.HORIZONTAL)
        vbox.Add(line, 0, wx.ALL | wx.EXPAND, 10)
        # vbox.Add((-1, 10))

        # LOGS
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)

        cleanconsolebutton = wx.Button(panel, label="Clear", id=APP_CLEAN_CONSOLE, size=(50, 30))
        font.SetPointSize(10)
        cleanconsolebutton.SetFont(font)
        hbox4.Add(cleanconsolebutton)

        cb = wx.CheckBox(panel, label="Verbose")
        cb.SetFont(font)
        hbox4.Add(cb, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL)

        st2 = wx.StaticText(panel, label='Logs')
        font.SetPointSize(12)
        st2.SetFont(font)
        hbox4.Add(st2, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL)
        vbox.Add(hbox4, border=10, flag=wx.ALL | wx.EXPAND)

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        tc2.SetEditable(False)
        font.SetPointSize(15)
        tc2.SetFont(font)
        # tc2.SetBackgroundColour((226, 238, 255))
        global USER_CONSOLE
        USER_CONSOLE = tc2
        hbox5.Add(tc2, proportion=1, flag=wx.EXPAND | wx.BOTTOM, border=5)
        vbox.Add(hbox5, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.EXPAND,
                 border=5)

        panel.SetSizer(vbox)

        # BINDINGS
        self.Bind(wx.EVT_MENU, self.on_quit, id=APP_EXIT)
        self.Bind(wx.EVT_MENU, self.on_help, id=APP_HELP_HINT)
        self.Bind(wx.EVT_BUTTON, self.on_quit, id=APP_EXIT)
        self.Bind(wx.EVT_BUTTON, lambda event: self.on_start(event, edittextfilein, edittextdirin, edittextdirout, cb),
                  btn1, id=APP_START)
        self.Bind(wx.EVT_BUTTON, lambda event: self.on_selected_input_file(event, edittextfilein), selectfileinbutton,
                  id=APP_SELECT_INPUT_FILE)
        self.Bind(wx.EVT_BUTTON, lambda event: self.on_selected_output_dir(event, edittextdirout), selectdiroutbutton,
                  id=APP_SELECT_OUTPUT_DIR)
        self.Bind(wx.EVT_BUTTON, lambda event: self.on_selected_output_dir(event, edittextdirin),
                  id=APP_SELECT_INPUT_DIR)
        self.Bind(wx.EVT_BUTTON, self.clean_console, id=APP_CLEAN_CONSOLE)

    @staticmethod
    def on_help(event):
        event.Skip()
        dial = wx.MessageDialog(None, HELP_MSG, 'Help', wx.OK | wx.ICON_QUESTION)
        dial.ShowModal()

    def on_quit(self, event):
        event.Skip()
        self.Close()

    def on_start(self, event, edittextfilein, edittextdirin, edittextdirout, checkboxverbose):
        event.Skip()

        input_file = edittextfilein.GetValue()
        input_dir = edittextdirin.GetValue()
        ouput_dir = edittextdirout.GetValue()
        verbose = checkboxverbose.GetValue()

        # CHECK INPUT
        if input_file is None or len(input_file) == 0 or not Path(input_file).exists():
            input_file = None

        if input_dir is None or len(input_dir) == 0 or not Path(input_dir).exists():
            input_dir = None

        if input_file is None and input_dir is None:
            self.__alert_on_error__("Error loading file: check if the input file exist!", "Wrong path")
            return

        # se esistono entrambi i path (input file e input directory), considero solo il path che punta ad una directory
        if input_dir is not None:
            input_file = input_dir

        # CHECK OUTPUT
        if ouput_dir is None or len(ouput_dir) == 0 or not Path(ouput_dir).exists():
            ouput_dir = None

        if ouput_dir is None:
            self.__alert_on_error__("Error: check if the output location exist!", "Wrong path")
            return

        # START OPERATION
        input_data = InputData(input_file, ouput_dir, None, verbose, True)
        init_operation(input_data)

    @staticmethod
    def __alert_on_error__(message, windows_name):
        dial = wx.MessageDialog(None, message, windows_name, wx.OK | wx.ICON_ERROR)
        dial.ShowModal()

    @staticmethod
    def on_selected_input_file(event, edittextfilein):
        event.Skip()
        path = wx.FileSelector(
            message="Select file or directory to parse",
            wildcard="File (*.txt,*.pdf,*.docx)|*.txt;*.pdf;*.docx",
            default_path=SystemConstants.APP_ABS_PATH
        )
        if path is not None:
            edittextfilein.SetValue(path)

    @staticmethod
    def on_selected_output_dir(event, edittextdirout):
        event.Skip()
        path = wx.DirSelector(
            message="Select output directory",
            default_path=SystemConstants.APP_ABS_PATH
        )

        if path is not None:
            edittextdirout.SetValue(path)

    @staticmethod
    def clean_console(event):
        event.Skip()
        if USER_CONSOLE is not None:
            USER_CONSOLE.SetValue("")

    def print_to_user(self, message=""):
        if USER_CONSOLE is not None and message is not None:
            USER_CONSOLE.AppendText(message + "\n")

    def get_user_input(self, question="", format_answere=""):
        dlg = wx.MessageDialog(None, question, style=wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal() == wx.ID_YES
        dlg.Destroy()
        return result
