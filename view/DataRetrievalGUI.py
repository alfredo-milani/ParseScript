import wx

from constants import SystemConstants
from view import DataRetrievalUI


class DataRetrievalGUI(wx.Frame, DataRetrievalUI):
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
        super(DataRetrievalGUI, self).__init__(
            parent,
            id=wx.ID_ANY,
            title=title,
            pos=wx.DefaultPosition,
            size=(900, 500)
        )

        # Objects that will be used
        self.__user_console = None
        self.__edittextfile = None
        self.__edittextdirinput = None
        self.__edittextdiroutput = None
        self.__checkboxverbose = None
        self.__controller_instance = None
        ###
        self.init_view()
        self.Centre()

    @property
    def user_console(self):
        return self.__user_console

    @user_console.setter
    def user_console(self, value):
        # PyCharm inspection bug
        self.__user_console = value

    @property
    def edittextfile(self):
        return self.__edittextfile

    @edittextfile.setter
    def edittextfile(self, value):
        # PyCharm inspection bug
        self.__edittextfile = value

    @property
    def edittextdirinput(self):
        return self.__edittextdirinput

    @edittextdirinput.setter
    def edittextdirinput(self, value):
        # PyCharm inspection bug
        self.__edittextdirinput = value

    @property
    def edittextdiroutput(self):
        return self.__edittextdiroutput

    @edittextdiroutput.setter
    def edittextdiroutput(self, value):
        # PyCharm inspection bug
        self.__edittextdiroutput = value

    @property
    def checkboxverbose(self):
        return self.__checkboxverbose

    @checkboxverbose.setter
    def checkboxverbose(self, value):
        # PyCharm inspection bug
        self.__checkboxverbose = value

    @property
    def controller_instance(self):
        return self.__controller_instance

    @controller_instance.setter
    def controller_instance(self, value):
        self.__controller_instance = value

    def init_view(self):
        # CREATE PANEL
        panel = wx.Panel(self)

        # SET ICON
        # ON PACKAGING remove "SystemConstants.APP_ABS_PATH + split_char() + " from the following icon's path.
        # ON PACKAGING on Windows system the icon must be in *.ico format;
        # after pyinstaller is executed move the executable in the root of the project.
        from utils import Converter
        icon = wx.Icon(
            SystemConstants.APP_ABS_PATH + Converter.split_char() +
            "resources" + Converter.split_char() +
            "images" + Converter.split_char() + "icon.png",
            wx.BITMAP_TYPE_PNG,
            512,
            512
        )
        self.SetIcon(icon)

        # MENU ITEMS
        menubar = wx.MenuBar()

        filemenu = wx.Menu()
        quitmenuitem = wx.MenuItem(filemenu, DataRetrievalGUI.APP_EXIT, '&Quit\tCtrl+Q')
        '''
        # ON WINDOWS viene mostrata non ridimensionata
        # ON UNIX systems (Debian) non viene mostrata
        quitmenuitem.SetBitmap(wx.Bitmap(os.path.join(
            SystemConstants.APP_ABS_PATH,
            "resources" + split_char() + "images" + split_char() + "exit.png"
        )))
        '''

        helpmenu = wx.Menu()
        helpmenuitem = wx.MenuItem(helpmenu, DataRetrievalGUI.APP_HELP_HINT, "&Help\tCtrl+H")

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
        self.__edittextfile = wx.TextCtrl(panel)
        buttonfileinput = wx.Button(panel, label="...", size=(50, 10), id=DataRetrievalGUI.APP_SELECT_INPUT_FILE)
        inputboxpathfileinput.Add(self.__edittextfile, flag=wx.RIGHT, border=10, proportion=1)
        inputboxpathfileinput.Add(buttonfileinput, flag=wx.EXPAND)

        inputstatictextchoose = wx.StaticText(panel, label="OR")
        inputstatictextchoose.SetFont(font)

        inputboxpathdirinput = wx.BoxSizer(wx.HORIZONTAL)
        self.__edittextdirinput = wx.TextCtrl(panel)
        buttondirinput = wx.Button(panel, label="...", size=(50, 10), id=DataRetrievalGUI.APP_SELECT_INPUT_DIR)
        inputboxpathdirinput.Add(self.__edittextdirinput, flag=wx.RIGHT, border=10, proportion=1)
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
        self.__edittextdiroutput = wx.TextCtrl(panel)
        buttondiroutput = wx.Button(panel, label="...", size=(50, 10), id=DataRetrievalGUI.APP_SELECT_OUTPUT_DIR)

        outputbox.Add(outputstatictext, flag=wx.RIGHT, border=10)
        outputbox.Add(self.__edittextdiroutput, flag=wx.RIGHT, border=10, proportion=1)
        outputbox.Add(buttondiroutput, flag=wx.EXPAND)

        mainbox.Add(outputbox, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # LINE SEPARATOR
        line = wx.StaticLine(panel, style=wx.HORIZONTAL)
        mainbox.Add(line, 0, wx.ALL | wx.EXPAND, 10)
        # mainbox.Add((-1, 10))

        # START / STOP BUTTONS
        manageoperationbox = wx.BoxSizer(wx.HORIZONTAL)

        buttonstart = wx.Button(panel, label='Start', size=(150, 30), id=DataRetrievalGUI.APP_START)
        buttonstart.SetFont(font)
        buttonclose = wx.Button(panel, label='Close', size=(150, 30), id=DataRetrievalGUI.APP_EXIT)
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

        buttoncleanconsole = wx.Button(panel, label="Clear", id=DataRetrievalGUI.APP_CLEAN_CONSOLE, size=(50, 30))
        buttoncleanconsole.SetFont(font)
        buttonshowfiles = wx.Button(panel, label="Files", id=DataRetrievalGUI.APP_SHOW_PARSED_FILES, size=(50, 30))
        buttonshowfiles.SetFont(font)
        self.__checkboxverbose = wx.CheckBox(panel, label="Verbose")
        self.__checkboxverbose.SetFont(font)
        statictextlogs = wx.StaticText(panel, label='Logs')
        font.SetPointSize(12)
        statictextlogs.SetFont(font)

        logbox.Add(buttoncleanconsole, flag=wx.ALIGN_CENTER_VERTICAL)
        logbox.Add(buttonshowfiles, flag=wx.ALIGN_CENTER_VERTICAL)
        logbox.Add(self.__checkboxverbose, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL)
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
        self.__user_console = edittextconsole

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
        self.Bind(
            wx.EVT_MENU,
            lambda event: self.__controller_instance.handle_quit(),
            id=DataRetrievalGUI.APP_EXIT
        )
        self.Bind(
            wx.EVT_MENU,
            lambda event: self.__controller_instance.handle_help(),
            id=DataRetrievalGUI.APP_HELP_HINT
        )
        self.Bind(
            wx.EVT_BUTTON,
            lambda event: self.__controller_instance.handle_quit(),
            id=DataRetrievalGUI.APP_EXIT
        )
        self.Bind(
            wx.EVT_BUTTON,
            lambda event: self.clear_console(),
            # button e id si possono anche usare in mutua esclusione
            # buttoncleanconsole,
            id=DataRetrievalGUI.APP_CLEAN_CONSOLE
        )
        self.Bind(
            wx.EVT_BUTTON,
            lambda event: self.__controller_instance.handle_start(),
            id=DataRetrievalGUI.APP_START
        )
        self.Bind(
            wx.EVT_BUTTON,
            lambda event: self.__controller_instance.handle_show_files(self.__edittextdiroutput.GetValue()),
            id=DataRetrievalGUI.APP_SHOW_PARSED_FILES
        )
        self.Bind(
            wx.EVT_BUTTON,
            lambda event: self.__controller_instance.handle_filename_selected(
                self.__edittextfile,
                "Select file to parse"
            ),
            id=DataRetrievalGUI.APP_SELECT_INPUT_FILE
        )
        self.Bind(
            wx.EVT_BUTTON,
            lambda event: self.__controller_instance.handle_directory_selected(
                self.__edittextdiroutput,
                "Select output directory"
            ),
            id=DataRetrievalGUI.APP_SELECT_OUTPUT_DIR
        )
        self.Bind(
            wx.EVT_BUTTON,
            lambda event: self.__controller_instance.handle_directory_selected(
                self.__edittextdirinput,
                "Select input directory"
            ),
            id=DataRetrievalGUI.APP_SELECT_INPUT_DIR
        )

    def print_to_user(self, message, message_type=DataRetrievalUI.Colors.TEXT_COLOR_DEFAULT):
        if self.__user_console and message:
            self.__user_console.SetForegroundColour(DataRetrievalGUI.ColorsGUI.get_color_from_code(message_type))
            self.__user_console.AppendText(message + "\n")
            self.__user_console.SetForegroundColour(DataRetrievalGUI.ColorsGUI.get_default_color())

    def clear_console(self):
        self.__controller_instance.handle_clear()

    def get_user_input_bool(self, question="", format_answere=""):
        dlg = wx.MessageDialog(None, question, style=wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal() == wx.ID_YES
        dlg.Destroy()
        return result

    class ColorsGUI(DataRetrievalUI.Colors):
        """
        Defining colors for GUI
        """

        CONSOLE_DEFAULT_COLOR = (DataRetrievalUI.Colors.TEXT_COLOR_DEFAULT, wx.WHITE)
        CONSOLE_WARNING_COLOR = (DataRetrievalUI.Colors.TEXT_COLOR_WARNING, wx.YELLOW)
        CONSOLE_ERROR_COLOR = (DataRetrievalUI.Colors.TEXT_COLOR_ERROR, wx.RED)
        CONSOLE_SUCCESS_COLOR = (DataRetrievalUI.Colors.TEXT_COLOR_SUCCESS, wx.GREEN)
        CONSOLE_START_OPERATION_COLOR = (DataRetrievalUI.Colors.TEXT_COLOR_START_OPERATION, wx.CYAN)

        CONSOLE_COLORS = [
            CONSOLE_DEFAULT_COLOR,
            CONSOLE_ERROR_COLOR,
            CONSOLE_SUCCESS_COLOR,
            CONSOLE_START_OPERATION_COLOR,
            CONSOLE_WARNING_COLOR
        ]

        def __init__(self):
            super(DataRetrievalGUI.ColorsGUI, self).__init__()

        @staticmethod
        def get_color_from_code(type_code):
            for color in DataRetrievalGUI.ColorsGUI.CONSOLE_COLORS:
                if color[0] == type_code:
                    return color[1]

            return DataRetrievalGUI.ColorsGUI.get_default_color()

        @staticmethod
        def get_default_color():
            return DataRetrievalGUI.ColorsGUI.CONSOLE_DEFAULT_COLOR[1]
