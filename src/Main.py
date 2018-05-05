#!/usr/bin/python
# ============================================================================
# Titolo:           Main.py
# Descrizione:      Script per estrapolare dati da un file ed inserirli in un file *.xlsx
# Autore:           Alfredo Milani (alfredo.milani.94@gmail.com)
# Data:             ven 20 ott 2017, 19.36.00, CEST
# Licenza:          MIT License
# Versione:         2.9.0
# Note:             --/--
# Versione bash:    4.4.12(1)-release
# ============================================================================
import sys

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
        from constants import APP_NAME

        graphical_interface = wx.App(False)

        controller = DataRetrievalGUIController()
        controller.view_instance = DataRetrievalGUI.build(APP_NAME)
        controller.view_instance.controller_instance = controller

        controller.view_instance.Show(True)
        graphical_interface.MainLoop()
    else:
        from view import DataRetrievalCLI
        from control import DataRetrievalCLIController

        controller = DataRetrievalCLIController()
        controller.view_instance = DataRetrievalCLI()

        controller.manage_operation(params)
