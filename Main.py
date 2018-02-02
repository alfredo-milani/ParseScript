#!/usr/bin/python
# ============================================================================
# Titolo:           Main.py
# Descrizione:      Script per estrapolare dati da un file ed inserirli in un file *.xlsx
# Autore:           Alfredo Milani (alfredo.milani.94@gmail.com)
# Data:             ven 20 ott 2017, 19.36.00, CEST
# Licenza:          MIT License
# Versione:         2.7.0
# Note:             --/--
# Versione bash:    4.4.12(1)-release
# ============================================================================
import sys

from constants import SystemConstants, APP_NAME
from utils import Common

if __name__ == "__main__":
    Common.set_up_sys()

    params = Common.parse_arg(sys.argv[1:])
    # FOR PACKAGING OPERATION UNCOMMENT THIS LINE AND COMMENT THE LINE ABOVE
    # params = Common.parse_arg(["--gui"])

    if params.gui:
        import wx
        from view import DataRetrievalGUI
        from control import DataRetrievalGUIController

        graphic_interface = wx.App(False)

        gui_view = DataRetrievalGUI(None, APP_NAME)
        controller = DataRetrievalGUIController()
        controller.view_instance = gui_view
        gui_view.controller_instance = controller

        SystemConstants.UI_CONSOLE = controller.view_instance
        SystemConstants.UI_CONSOLE.Show(True)
        graphic_interface.MainLoop()
    else:
        from view import DataRetrievalCLI
        from control import DataRetrievalCLIController

        cli_view = DataRetrievalCLI()
        controller = DataRetrievalCLIController()

        SystemConstants.UI_CONSOLE = cli_view
        controller.manage_operation(params)
